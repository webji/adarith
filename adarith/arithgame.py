#!/usr/bin/env python

"""
A basket ball game
"""


VERSION = '0.1'

try:
    import sys, random, math, os, getopt
    import pygame
    from socket import *
    from pygame.locals import *
    import sqlalchemy as sa
    from sqlalchemy.orm import sessionmaker

    from lib.scene import SceneBase
    from lib.game import GameBase
    from lib.utils import *
    from lib.operation import OperationType
    from lib.arithmetic import ArithmeticFactory
    from lib.question import QuestionStatus, Question, ArithQuestion
    from lib.exam import Exam
    from lib.sound import Sound
    from lib.image import Image
    from lib.voicer import Voicer

    # from model import Base
    # from model.user_model import UserModel
    # from model.setting_model import SettingModel
    # from model.question_model import QuestionModel

except ImportError as e:
    print(f'Failed to load module: {e}')
    sys.exit(2)



class TitleScene(SceneBase):
    def __init__(self, id='title_scene', name='Title Sene', bg_color=(0,0,0), bg_image=None, bg_music=None):
        # self.tts_engine = None
        self.voicer = None
        super().__init__(id=id, name=name, bg_color=bg_color, bg_image=bg_image, bg_music=bg_music)

    
    def _pre_enter(self, **kwarg):
        super()._pre_enter(**kwarg)
        self.voicer.sayTTS("Hello, Ada. Welcome to Your Arithmeic World!")
        

    def draw(self, screen):
        # screen.fill(DEFAULT_BACKGROUND)
        WIDTH, HEIGHT = screen.get_size()
        draw_text(screen, "GET READY", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <space> to start", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        draw_text(screen, "press <m> for menu", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 50, align="center")


class ArithExam(Exam):
    def __init__(self):
        self.operation = OperationType()
        self.arithmeticFactory = ArithmeticFactory()
        
        super().__init__()

    def add(self, question):
        if question.status != QuestionStatus.COMPLETED:
            self.incompleted_questions[question.id] = question
            self.completed_questions.pop(question.id, None)
        else:
            self.completed_questions[question.id] = question
            self.incompleted_questions.pop(question.id, None)

    def load(self):
        self.number += 1
        for i in range(0, 9):
            arithmetic = self.arithmeticFactory.buildAritmetic(self.operation)
            question = ArithQuestion(f'arith_{i}', i, arithmetic)
            self.add(question)
        
    

    def next(self):
        if self.question != None:
            self.add(self.question)
            self.question = None

        if self.is_completed == False:
            self.question = self.incompleted_questions[sorted(self.incompleted_questions.keys())[0]]
        return self.question
    
    @property
    def is_completed(self):
        return len(self.incompleted_questions.keys()) == 0 and self.question == None 

    
    def draw(self, screen):
        # screen.fill(DEFAULT_BACKGROUND)
        WIDTH, HEIGHT = screen.get_size()
        left_tab_x = WIDTH/10
        left_tab_y = HEIGHT*2/5

        exam_number = f'Exam      : {self.number}'
        draw_text(screen, exam_number, 30, GREEN, left_tab_x, left_tab_y, align='center')
        left_tab_y += 35

        exam_total = f'Total     : {self.total_count}'
        draw_text(screen, exam_total, 30, GREEN, left_tab_x, left_tab_y, align='center')
        left_tab_y += 35

        exam_complete = f'Complete  : {self.complete_count}'
        draw_text(screen, exam_complete, 30, GREEN, left_tab_x, left_tab_y, align='center')
        left_tab_y += 35

        exam_remains = f'Remain    : {self.incomplete_count}'
        draw_text(screen, exam_remains, 30, GREEN, left_tab_x, left_tab_y, align='center')
        left_tab_y += 35

        exam_correct = f'Correct   : {self.result_count(True)}'
        draw_text(screen, exam_correct, 30, GREEN, left_tab_x, left_tab_y, align='center')
        left_tab_y += 35

        exam_wrong = f'Wrong     : {self.result_count(False)}'
        draw_text(screen, exam_wrong, 30, RED, left_tab_x, left_tab_y, align='center')
        left_tab_y += 35

        question_status = f'{self.question.status}'
        draw_text(screen, question_status, 20, GREEN, left_tab_x, left_tab_y, align='center')    

        question_tab_x = WIDTH//2
        question_tab_y = HEIGHT/6

        draw_text(screen, f'Please Input the Result', 50, WHITE, question_tab_x , question_tab_y, align='center')
        question_tab_y += 60
        
        question_number = f'Question  : {self.question.number}'
        draw_text(screen, question_number, 30, WHITE, question_tab_x , question_tab_y, align='center')
        question_tab_y += 100

        draw_text(screen, f'{self.question}', 150, WHITE, question_tab_x, question_tab_y, align="center")
        question_tab_y += 180

        question_color = WHITE if self.question.result == None else RED if self.question.result == False else GREEN  
        draw_text(screen, f'{self.question.answer}', 200, question_color, question_tab_x, question_tab_y, align="center")
        question_tab_y += 210

        draw_text(screen, "press <q> to end", 20, WHITE, question_tab_x, HEIGHT * 3 / 4, align="center")
    
        

class ArithScene(SceneBase):
    def __init__(self, id='arith_scene', name='Arith Sene', bg_color=(0,0,0), bg_image=None, bg_music=None):
        self.exam = ArithExam()
        self.exam.load()
        self.question = self.exam.next()
        # self.tts_engine = None
        self.voicer = None
        self.right_image = None
        self.wrong_image = None
        super().__init__(id=id, name=name, bg_color=bg_color, bg_image=bg_image, bg_music=bg_music)

    def draw(self, screen):
        self.exam.draw(screen)

        if self.question.status == QuestionStatus.GRADED and self.question.result != None:
            if self.question.result == True:
                img_rect = self.right_image.get_rect()
                img_rect.center = (800, 450)
                screen.blit(self.right_image, img_rect)
            else:
                img_rect = self.wrong_image.get_rect()
                img_rect.center = (800, 450)
                screen.blit(self.wrong_image, img_rect)
        

    def _handle_scene_event(self, event):
        if self.question != None:
            if self.question.status == QuestionStatus.STARTED:
                if event.type == KEYUP and event.key in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                    key = event.key - 48
                    self.question.answering(key)
            elif self.question.status == QuestionStatus.ANSWERED:
                if event.type == KEYUP:
                    if event.key == K_RETURN:
                        self.question.submit()
                        if self.question.result == True:
                            self.voicer.sayTTS("Well done!")
                        else:
                            self.voicer.sayTTS("Sorry!")
                    elif event.key in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                        key = event.key - 48
                        value = self.question.answer*10 + key
                        self.question.answering(value)
                    elif event.key == K_ESCAPE:
                        self.question.answering(0)

            elif self.question.status == QuestionStatus.GRADED:
                if event.type == KEYUP and event.key in [K_RIGHT, K_SPACE, K_RETURN]:
                    self.question.complete()
                    self.exam.add(self.question)
                    self.question = None
            elif self.question.status == QuestionStatus.COMPLETED:
                if event.type == KEYUP and event.key in [K_RIGHT, K_SPACE, K_RETURN]:
                    key = event.key - 48
                    self.question = self.exam.next()

        return super()._handle_scene_event(event)


    def update(self):
        if (self.question == None) or self.question.status == QuestionStatus.COMPLETED:
            if self.exam.is_completed == False:
                self.question = self.exam.next()
        if self.question == None:
            if self.exam.operation.type == OperationType.ADD:
                self.exam.operation = OperationType(OperationType.SUB)
            else:
                self.exam.operation = OperationType(OperationType.ADD)
            self.exam.load()
            self.question = self.exam.next()

        if self.question.status == QuestionStatus.INITED:
            self.question.start()
            self.voicer.saySimple(f'{self.question}')
        
        return super().update()


class MenuScene(SceneBase):
    def __init__(self, id='menu_scene', name='Menu Sene', bg_color=(0,0,0), bg_image=None, bg_music=None):
        self.voider = None
        super().__init__(id=id, name=name, bg_color=bg_color, bg_image=bg_image, bg_music=bg_music)


    def draw(self, screen):
        # screen.fill(DEFAULT_BACKGROUND)
        WIDTH, HEIGHT = screen.get_size()
        draw_text(screen, "SETTINGS", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <ESC> to return", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")


class EndScene(SceneBase):
    def __init__(self, id='end_scene', name='End Sene', bg_color=(0,0,0), bg_image=None, bg_music=None):
        self.voicer = None
        super().__init__(id=id, name=name, bg_color=bg_color, bg_image=bg_image, bg_music=bg_music)


    def _handle_scene_event(self, event):
        super()._handle_scene_event(event)
        if event.type == KEYDOWN and event.key == K_q:
            self.voicer.sayTTS("Goodbye Ada, my honor to see next time")
            self.end()
            self.voicer.end()
            sys.exit(0)


    def draw(self, screen):
        # screen.fill(DEFAULT_BACKGROUND)
        WIDTH, HEIGHT = screen.get_size()
        draw_text(screen, "GAME OVER", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <r> to restart", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        draw_text(screen, "press <q> to exit", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 30, align="center")


class ArithGame(GameBase):

    def _init_db(self):
        db_engine = sa.create_engine(f'sqlite:///{os.path.join(self.main_dir, "data/adarith.db?check_same_hread=False")}', echo=True)
        Base.metadata.create_all(db_engine)
        db_session = sessionmaker(bind=db_engine)
        self.db_session = db_session()
        UserModel.init_user(self.db_session)
        SettingModel.init_setting(self.db_session)
        QuestionModel.init_question(self.db_session)

        
    def _init_res(self):
        super()._init_res()
        self.key_sound = Sound(os.path.join(self.sound_dir, 'pew.wav'))
        self.bg_image = Image(os.path.join(self.image_dir, 'blackboard_1024_768.png')).image
        self.right_image = Image(os.path.join(self.image_dir, 'right_140_147.png')).image
        self.wrong_image = Image(os.path.join(self.image_dir, 'wrong_140_177.png')).image

        # self._init_db()

        self.voicer_name = 'ada'
        self.voice_path = os.path.join(self.sound_dir, self.voicer_name)
        self.voicer = Voicer(path = self.voice_path)

        

    def _init_scenes(self):
        happyTune = os.path.join(self.sound_dir, 'Happy Tune.ogg')
        titleScene = TitleScene(bg_music=happyTune)
        # titleScene.tts_engine = self.engine
        titleScene.voicer = self.voicer

        arithScene = ArithScene(bg_music=happyTune)
        # arithScene.tts_engine = self.engine
        arithScene.voicer = self.voicer
        arithScene.right_image = self.right_image
        arithScene.wrong_image = self.wrong_image

        menuScene = MenuScene(bg_music=happyTune)
        menuScene.voicer = self.voicer

        yippee = os.path.join(self.sound_dir, 'Yippee.ogg')
        endScene = EndScene(bg_music=yippee)
        endScene.voicer = self.voicer

        titleScene.add_next(K_ESCAPE, endScene).add_next(K_m, menuScene).add_next(K_SPACE, arithScene)
        menuScene.add_next(K_ESCAPE, titleScene)
        arithScene.add_next(K_q, endScene)
        endScene.add_next(K_r, titleScene)

        self.scene = titleScene
        
        return super()._init_scenes()


    def _pre_run(self, **kwargs):
        super()._pre_run(**kwargs)
        self.scene.switch_to(self.scene)



    