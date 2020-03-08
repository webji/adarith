
import os, threading, time
from enum import Enum

import pygame as pg
import pyttsx3 as pt

from .sound import Sound
from .utils import *



class ThreadTask(object):
    def __init__(self):
        self._running = True
        super().__init__()

    def end(self):
        print('Set _running: False - {self}')
        self._running = False

    def run(self, **kwargs):
        pass

class ChannelTask(ThreadTask):
    
    def run(self, channel=None, play_list=None, play_list_lock=None, delay=0.5):
        sound = None
        while self._running:
            print('ChannelTask Running')
            if channel.get_busy() == False:
                with play_list_lock:
                    if len(play_list) > 0:
                        sound = play_list.pop()
                    else:
                        sound = None
                
                if sound != None:
                    channel.play(sound)
                
            time.sleep(delay)
        print('ChannelTask Return')
        return
        

class TTSTask(ThreadTask):
    def __init__(self):
        self.engine = None
        super().__init__()

    def end(self):
        self.engine.endLoop()
        return super().end()

    def run(self, engine=None, tts_list=None, tts_list_lock=None, delay=0.5):
        sentence = None
        self.engine = engine
        while self._running:
            with tts_list_lock:
                if len(tts_list) > 0:
                    sentence = tts_list.pop()
                else:
                    sentence = None

            if sentence != None:
                engine.say(sentence)
                engine.runAndWait()
                               
        time.sleep(delay)



class Voicer(object):
    def __init__(self, path=''):
        self.path = path
        self.number_sounds = []
        self.plus_sound = Sound(os.path.join(path, '+.wav')).sound
        self.minus_sound = Sound(os.path.join(path, '-.wav')).sound
        self.equal_sound = Sound(os.path.join(path, '=.wav')).sound
        self.shi_sound = Sound(os.path.join(path, 'shi2.wav')).sound
        self.ji_sound = Sound(os.path.join(path, 'ji3.wav')).sound
        self._init_numbers()

        self.channel = self._find_channel()
        self.play_list = []
        self.play_list_lock = threading.Lock()
        self.channel_task = ChannelTask()
        self.play_thread = threading.Thread(None, self.channel_task.run, args=(self.channel, self.play_list, self.play_list_lock), daemon=True)
        self.play_thread.start()
        
        self.engine = pt.init()
        self.engine.setProperty('rate', 120)
        self.engine.setProperty('volume', 1)
        self.tts_list = []
        self.tts_list_lock = threading.Lock()
        self.tts_task = TTSTask()
        self.tts_thread = threading.Thread(None, self.tts_task.run, args=(self.engine, self.tts_list, self.tts_list_lock), daemon=True)
        self.tts_thread.start()

        super().__init__()

    def queue(self, sound):
        with self.play_list_lock:
            self.play_list.insert(0, sound)
        

    def queue_tts(self, sentence):
        with self.tts_list_lock:
            self.tts_list.insert(0, sentence)
            

    def _find_channel(self):
        n = pg.mixer.get_num_channels()
        print(f'Found Channel: {n}')
        for i in range(n):
            channel = pg.mixer.Channel(i)
            if channel.get_busy() == False:
                print(f'Use Channel: {i}')
                return channel

    def _init_numbers(self):
        for i in range(10):
            sound = Sound(os.path.join(self.path, f'{i}.wav')).sound
            self.number_sounds.append(sound)


    def say_0_99(self, number = 1):
        if number >=0 and number < 10:
            self.queue(self.number_sounds[number])
        if number >= 10 and number < 99:
            h_number = number / 10
            l_number = number % 10
            if h_number != 1:
                self.queue(self.number_sounds[number])
            self.queue(self.shi_sound)
            if l_number != 0:
                self.queue(self.number_sounds[number])     


    def sayWord(self, word = '1'):
        if word == '+':
            self.queue(self.plus_sound)
        elif word == '-':
            self.queue(self.minus_sound)
        elif word == '=':
            self.queue(self.equal_sound)
        elif word in ['?', 'ji3']:
            self.queue(self.ji_sound)
        elif word == 'shi2':
            self.queue(self.shi_sound)
        elif is_digit(word) or (len(word) == 2 and is_digit(word[0]) and is_digit(word[1])):
            self.say_0_99(int(word))
        else:
            self.say_0_99(0)


    def saySimple(self, sentence='1+1=2'):
        words = sentence
        print(f'{sentence}')
        if '+' in sentence:
            words = words.split('+')
            self.sayWord(words[0].strip())
            self.sayWord('+')
        elif '-' in sentence:
            words = words.split('-')
            self.sayWord(words[0].strip())
            self.sayWord('-')
        words = words[1].split('=')
        self.sayWord(words[0].strip())
        self.sayWord('=')
        self.sayWord(words[1].strip())
            
    def sayTTS(self, sentence='Hello Ada'):
        self.queue_tts(sentence=sentence)

    
    def end(self):
        print('Try to end Voicer')
        self.channel_task.end()
        self.tts_task.end()
        self.play_thread.join()
        self.tts_thread.join()

        

