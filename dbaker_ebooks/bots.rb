#!/usr/bin/env ruby

require 'twitter_ebooks'
include Ebooks

AUTH = JSON.parse(File.read("resources/auth.json"), symbolize_names: true)
CONSUMER_KEY = AUTH[:consumer_key]
CONSUMER_SECRET = AUTH[:consumer_secret]
OATH_TOKEN = AUTH[:oauth_token] # oauth token for ebooks account
OAUTH_TOKEN_SECRET = AUTH[:oauth_token_secret] # oauth secret for ebooks account
ROBOT_ID = /ebooks|horse/ # Avoid infinite reply chains
TWITTER_USERNAME = "dbaker_bat" # Ebooks account username
TEXT_MODEL_NAME = "dorotheabaker" # This should be the name of the text model

DELAY = 3..40 # Simulated human reply delay range in seconds
BLACKLIST = [] # Grumpy users to avoid interaction with

SPECIAL_WORDS = []
SPECIAL_USERS = []
BORING_WORDS = []

File.foreach("resources/bffs.txt") {|el| SPECIAL_USERS.push(el) }
File.foreach("resources/special.txt") {|el| SPECIAL_WORDS.push(el) }
File.foreach("resources/boring.txt") {|el| BORING_WORDS.push(el) }

UNICODES = ["\u0308", "\u0324", "\u0300", "\u0301", "\u0307", "\u030a", "\u0325", "\u0360", "\u0361", "\u0338", "\u0363", "\u0364", "\u0365", "\u0366", "\u0367", "\u0368", "\u0369", "\u036a", "\u036c", "\u036d", "\u036e", "\u036f", "\u035c", "\u0325", "\u0323"
]

# Track who we've randomly interacted with globally
$have_talked = {}

class GenBot
  def initialize(bot, modelname)
    @bot = bot
    @model = nil

    @following = []

    bot.consumer_key = CONSUMER_KEY
    bot.consumer_secret = CONSUMER_SECRET
  
    bot.on_startup do
      @model = Model.load("model/#{modelname}.model")
      @top100 = @model.keywords.top(100).map(&:to_s).map(&:downcase)
      @top20 = @model.keywords.top(20).map(&:to_s).map(&:downcase)
    end
  
  # TODO
  #def boring?(text)
  #   tokens = Ebooks::NLP.tokenize(text.downcase.gsub "\u2019", "'")
  #   !!(tokens.find { |t| BORING_WORDS.include? t })
  #end
  
  #bot.on_message do |dm|
  #   bot.delay DELAY do
  #     bot.reply dm, @model.make_response(dm[:text])
  #   end
  #end
  
    bot.on_follow do |user|
      interesting = SPECIAL_USERS.include?(user) || user.downcase.include?("ebooks") || user.downcase.include?("bot")
      if interesting && !(@following.include? username)
        bot.delay DELAY do
          bot.follow user[:screen_name]
          @following << username
        end
      end
    end
  
    bot.on_mention do |tweet, meta|
      # Avoid infinite reply chains (very small chance of crosstalk)
      next if tweet[:user][:screen_name].match(ROBOT_ID) && rand > 0.05
  
      tokens = NLP.tokenize(tweet[:text])
      very_interesting = tokens.find_all { |t| @top100.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t.downcase) }
  
      if very_interesting || special
        favorite(tweet)
      end
  
      reply(tweet, meta)

    end
  
    bot.on_timeline do |tweet, meta|
      next if tweet[:retweeted_status] || tweet[:text].start_with?('RT')
      #next if BLACKLIST.include?(tweet[:user][:screen_name])
  
      tokens = NLP.tokenize(tweet[:text])
  
      # We calculate unprompted interaction probability by how well a
      # tweet matches our keywords
      interesting = tokens.find { |t| @top100.include?(t.downcase) }
      very_interesting = tokens.find_all { |t| @top20.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t.downcase) }
  
      interesting = special || interesting || very_interesting || (SPECIAL_USERS.include?(tweet[:user][:screen_name]))

      if interesting && rand(10) <= 4
        favorite(tweet)
        favd = true # Mark this tweet as favorited
  
        bot.delay DELAY do
          bot.follow tweet[:user][:screen_name]
        end
      end
  
      # Any given user will receive at most one random interaction per day
      # (barring special cases)
      next if $have_talked[tweet[:user][:screen_name]]
      $have_talked[tweet[:user][:screen_name]] = true
  
      if very_interesting || special
        favorite(tweet) if (rand < 0.5 && !favd) # Don't fav the tweet if we did earlier
        #retweet(tweet) if rand < 0.1
        reply(tweet, meta) if rand < 0.1
      elsif interesting
        favorite(tweet) if rand < 0.1
        #reply(tweet, meta) if rand < 0.05
      end
    end
  
    bot.scheduler.every '15m', :first_in => '5s' do
      next if rand(10) == 0
  
      tweet = @model.make_statement
  
      (0..10).each do
        if verbatim_text?(tweet) then
          tweet = @model.make_statement
        end
      end
  
      tokens = NLP.tokenize(tweet)
  
      very_interesting = tokens.find_all { |t| @top100.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t.downcase) }
  
      if very_interesting || special

        if rand < 0.1
          tweet = move_letters_around(tweet)
        #elsif rand < 0.4
        #  tweet = move_words_around(tweet)
        end

        if rand < 0.2
            diacritic(tweet)
        end

        @bot.tweet tweet

      elsif rand(10) <= 2

        if rand < 0.1
          tweet = move_letters_around(tweet)
        #elsif rand < 0.4
        #  tweet = move_words_around(tweet)
        end

        if rand < 0.2
            diacritic(tweet)
        end
        @bot.tweet tweet

      else
        @bot.log "not tweeting \"#{tweet}\", too boring (maybe?)"
      end
  
      #$have_talked = {}
    end
  end
  
  def reply(tweet, meta)
    resp = @model.make_response(meta[:mentionless], meta[:limit])
  
    (0..10).each do
      if verbatim_text?(resp) then
        resp = @model.make_response(meta[:mentionless], meta[:limit])
      end
    end
  
    tokens = NLP.tokenize(resp)

    very_interesting = tokens.find_all { |t| @top100.include?(t.downcase) }.length > 2
    special = tokens.find { |t| SPECIAL_WORDS.include?(t.downcase) }
    bff = SPECIAL_USERS.include?(tweet[:user])

    if rand < 0.1
      resp = move_letters_around(resp)
    #elsif rand < 0.4
    #  resp = move_words_around(resp)
    end

    # special delay for replies dependant on length of tweet
    len = resp.length
    if len < 80
      reply_delay = 3..9
    elsif len > 80 && len < 100
      reply_delay = 10..20
    else
      reply_delay = 20..40
    end

    if (very_interesting || special) || bff
      @bot.delay reply_delay do
        if rand < 0.2
            diacritic(resp)
        end

        @bot.reply tweet, meta[:reply_prefix] + resp
        @bot.log "Responded to #{tweet[:user]} with #{resp}"
      end
    elsif rand(10) <= 8
      @bot.delay reply_delay do
        if rand < 0.2
            diacritic(resp)
        end

        @bot.reply tweet, meta[:reply_prefix] + resp
        @bot.log "Responded to #{tweet[:user]} with #{resp}"
      end
    else
      @bot.log "abandoning conversation cause bored"
      favorite(tweet) # if last mention not replied to, fave it instead (just to be nice)
    end

  end
  
  def favorite(tweet)
    @bot.log "Favoriting @#{tweet[:user][:screen_name]}: #{tweet[:text]}"
    @bot.delay DELAY do
      @bot.twitter.favorite(tweet[:id])
    end
  end
  
  def retweet(tweet)
    @bot.log "Retweeting @#{tweet[:user][:screen_name]}: #{tweet[:text]}"
    @bot.delay DELAY do
      @bot.twitter.retweet(tweet[:id])
    end
  end

  ################################# glitching #################################

  # word and letter shifting code by Liam Cooke
  def move_letters_around(string)
    len = string.length
    char = ' '
    while char == ' '
      i = rand(len)
      char = string[i]
    end
    string = string[0...i] + string[i + 1...len]
    j = i
    while j == i
      j = rand(len)
    end
    string.insert(j, char)
    return string
  end

  def move_words_around(text)
    words = text.split
    len = words.length
    i = rand len
    w = words[i]
    words = words[0...i] + words[i + 1...len]
    words.insert(rand(len), w)
    string = words.join(' ')
    return string
    end
  end

  def diacritic(text)
    words = text.split
    len = words.length

    5.times do
        word = rand (len) # random word from string
        l = words[word].length
        char = rand (l) # random char from word

        if words[word][char].match /[[:alpha:]]/
            text.insert((char + 1) * (word + 1), UNICODES.sample)
        end
        puts(text)
    end

    return text
  end

  # fix verbatim for strings (also Liam's)
  def verbatim_text?(text)
    tokens = Ebooks::NLP.tokenize(text)
    @model.verbatim? tokens
  end
  #############################################################################

def make_bot(bot, modelname)
  GenBot.new(bot, modelname)
end

Ebooks::Bot.new(TWITTER_USERNAME) do |bot|
  bot.oauth_token = OATH_TOKEN
  bot.oauth_token_secret = OAUTH_TOKEN_SECRET

  make_bot(bot, TEXT_MODEL_NAME)
end
