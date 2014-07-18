#!/usr/bin/env ruby

require 'twitter_ebooks'
include Ebooks

AUTH = JSON.parse(File.read("auth.json"), symbolize_names: true)
CONSUMER_KEY = AUTH[:consumer_key]
CONSUMER_SECRET = AUTH[:consumer_secret]
OATH_TOKEN = AUTH[:oauth_token] # oauth token for ebooks account
OAUTH_TOKEN_SECRET = AUTH[:oauth_token_secret] # oauth secret for ebooks account
ROBOT_ID = "ebooks" # Avoid infinite reply chains
TWITTER_USERNAME = "dbaker_ebooks" # Ebooks account username
TEXT_MODEL_NAME = "dorotheabaker" # This should be the name of the text model

DELAY = 2..30 # Simulated human reply delay range in seconds
BLACKLIST = [] # Grumpy users to avoid interaction with

# TODO put wordlists etc in separate file and import
#SPECIAL_WORDS = ["bot", "b o t", "metal", "Bach", "minimalism", "omg"]
# SPECIAL_USERS = ["horse_inky", "inky", "thricedotted", "thricebotted", "katierosepipkin", "negatendo", "negatendo_ebooks", "wikisext", "oliviataters", "mstea_ebooks"]

SPECIAL_WORDS = []
SPECIAL_USERS = []
BORING_WORDS = []

File.foreach("resources/bffs.txt") {|el| SPECIAL_USERS.push(el) }
File.foreach("resources/special.txt") {|el| SPECIAL_WORDS.push(el) }
File.foreach("resources/boring.txt") {|el| BORING_WORDS.push(el) }

# Track who we've randomly interacted with globally
$have_talked = {}

class GenBot
  def initialize(bot, modelname)
    @bot = bot
    @model = nil
  
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
      if SPECIAL_USERS.include?(user) || user.downcase.include?("ebooks") || user.downcase.include?("bot")
        bot.delay DELAY do
          bot.follow user[:screen_name]
        end
      end
    end
  
    bot.on_mention do |tweet, meta|
      # Avoid infinite reply chains (very small chance of crosstalk)
      next if tweet[:user][:screen_name].include?(ROBOT_ID) && rand > 0.05
  
      tokens = NLP.tokenize(tweet[:text])
      very_interesting = tokens.find_all { |t| @top100.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t) }
  
      if very_interesting || special
        @bot.favorite(tweet)
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
      very_interesting = tokens.find_all { |t| @top50.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t) }
  
      if special || (SPECIAL_USERS.include?(tweet[:user][:screen_name]) && rand(10) < 2)
        @bot.favorite(tweet)
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
        @bot.favorite(tweet) if (rand < 0.5 && !favd) # Don't fav the tweet if we did earlier
        #retweet(tweet) if rand < 0.1
        reply(tweet, meta) if rand < 0.1
      elsif interesting
        @bot.favorite(tweet) if rand < 0.1
        #reply(tweet, meta) if rand < 0.05
      end
    end
  
    bot.scheduler.every '15m', :first_in => '5s' do
      next if rand(10) <= 0
  
      tweet = @model.make_statement
  
      (0..10).each do
        if @model.verbatim?(tweet) then
          tweet = @model.make_statement
        end
      end
  
      tokens = NLP.tokenize(tweet)
  
      very_interesting = tokens.find_all { |t| @top100.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t) }
  
      if very_interesting || special
        @bot.tweet tweet
      elsif rand(10) <= 3
        @bot.tweet tweet
      else
        @bot.log "not tweeting \"#{tweet}\", too boring (maybe?)"
      end
  
      #$have_talked = {}
    end #huh?
  end
  
    def reply(tweet, meta)
      resp = @model.make_response(meta[:mentionless], meta[:limit])
  
      (0..10).each do
        if @model.verbatim?(resp) then
          resp = @model.make_response(meta[:mentionless], meta[:limit])
        end
      end
  
      tokens = NLP.tokenize(resp)

      very_interesting = tokens.find_all { |t| @top100.include?(t.downcase) }.length > 2
      special = tokens.find { |t| SPECIAL_WORDS.include?(t) }
      bff = SPECIAL_USERS.include?(tweet[:user])
  
      if (very_interesting || special) || bff
        @bot.delay DELAY do
          @bot.reply tweet, meta[:reply_prefix] + resp
          @bot.log "Responded to #{tweet[:user]} with #{resp}"
        end
      elsif rand(10) <= 8
        @bot.delay DELAY do
          @bot.reply tweet, meta[:reply_prefix] + resp
          @bot.log "Responded to #{tweet[:user]} with #{resp}"
        end
      else
        @bot.log "abandoning conversation cause bored"
        @bot.favorite meta # if last mention not replied to, fave it instead (just to be nice)
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
  end # huh?

  def make_bot(bot, modelname)
    GenBot.new(bot, modelname)
  end

  Ebooks::Bot.new(TWITTER_USERNAME) do |bot|
    bot.oauth_token = OATH_TOKEN
    bot.oauth_token_secret = OAUTH_TOKEN_SECRET

    make_bot(bot, TEXT_MODEL_NAME)
  end
