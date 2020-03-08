
import os, threading, time
from enum import Enum

import pygame as pg
import pyttsx3 as pt

from .sound import Sound
from .utils import *


def play_thread(channel, play_list, play_list_lock, delay, play_thread_stop):
    sound = None
    # print('Starting Thread')
    while play_thread_stop == False:
        if channel.get_busy() == False:
            # print('Not Busy')
            play_list_lock.acquire()
            if len(play_list) > 0:
                sound = play_list.pop()
            else:
                sound = None
            play_list_lock.release()
            if sound != None:
                # print(f'Playing: {sound}')
                channel.play(sound)
            else:
                # print('No Sound')
                sound = None
                # return
        
        time.sleep(delay)
        

def tts_thread(engine, tts_list, tts_list_lock, tts_thread_stop):
    sentence = None
    while tts_thread_stop == False:
        tts_list_lock.acquire()
        if len(tts_list) > 0:
            sentence = tts_list.pop()
        else:
            sentence = None
        tts_list_lock.release()

        if sentence != None:
            engine.say(sentence)
            engine.runAndWait()
        else:
            sentence = None
            # return


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
        self.play_thread_stop = False
        self.play_thread = threading.Thread(None, play_thread, args=(self.channel, self.play_list, self.play_list_lock, 0.1, self.play_thread_stop))
        
        self.engine = pt.init()
        self.engine.setProperty('rate', 120)
        self.engine.setProperty('volume', 1)
        self.tts_list = []
        self.tts_list_lock = threading.Lock()
        self.tts_thread_stop = False
        self.tts_thread = threading.Thread(None, tts_thread, args=(self.engine, self.tts_list, self.tts_list_lock, self.tts_thread_stop))
        super().__init__()

    def queue(self, sound):
        self.play_list_lock.acquire()
        self.play_list.insert(0, sound)
        self.play_list_lock.release()
        if self.play_thread.is_alive() != True:
            self.play_thread.start()


    def queue_tts(self, sentence):
        self.tts_list_lock.acquire()
        self.tts_list.insert(0, sentence)
        self.tts_list_lock.release()
        if self.tts_thread.is_alive() == False:
            self.tts_thread.start()

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
        self.play_thread_stop = True
        self.tts_thread_stop = True
        self.play_thread.join()
        self.tts_thread.join()

        

