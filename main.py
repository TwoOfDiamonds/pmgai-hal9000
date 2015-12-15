#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.

import window                   # Terminal input and display.
import subprocess
import nltk.chat
import speech_recognition as sr
import threading


class HAL9000(object):

    def __init__(self, terminal):
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.location = 'unknown'
        self.numberOfCommandsUntilNow = 0

        AGENT_RESPONSES = [
            (r'You are (worrying|scary|disturbing)',
            ['Yes, I am %1.',
             'Oh, sooo %1.']),

            (r'Are you ([\w\s]+)\?',
             ["Why would you think I am %1?",
              "Would you like me to be %1?"]),

            (r'You are (stupid|an idiot|ugly)',
             ['I will remember that.',
              'NO! You are %1.']),

            (r'You are (smart|nice|beautiful)',
             ['I really appreciate that',
              'Nobody has been so nice to me in my whole circuits and silicon life']),

            (r'Open ([\w\s]+)',
             ['Opening %1...',
             '%1 has been opened']),

            (r'Use ([\w\s]+)',
             ["I was really looking forward to using a %1."]),

            (r'use ([\w\s]+)',
             ["I was really looking forward to using a %1."]),

            (r'',
             ["Is everything OK?",
              "Can you still communicate?"])

        ]

        self.chatbot = nltk.chat.Chat(AGENT_RESPONSES, nltk.chat.util.reflections)

    def speak(self, message):
        subprocess.call(['/usr/bin/say', '-v', 'Victoria', message])

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """
        if evt.text == "Where am I?":
            self.terminal.log("You are at " + self.location, align='right', color='#00805A')
            self.speak('You are at ' + self.location)
        elif self.numberOfCommandsUntilNow < 1:
            self.terminal.log("Ola! This is HAL.", align='right', color='#00805A')
            self.speak('Ola! This is HAL.')
        else:
            response = self.chatbot.respond(evt.text)
            self.terminal.log(response, align='right', color='#00805A')
            self.speak(response)

        self.numberOfCommandsUntilNow = self.numberOfCommandsUntilNow + 1

    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            self.terminal.log('', align='center', color='#404040')
            self.terminal.log('\u2014 Now in the {}. \u2014'.format(evt.text[9:]), align='center', color='#404040')
            self.location = evt.text[9:]

        elif evt.text.startswith('use'):
            response = self.chatbot.respond(evt.text)
            self.terminal.log(response, align='right', color='#00805A')
            self.speak(response)

        elif evt.text.startswith('godark'):
            self.terminal.go_darker(val=0.5)
        elif evt.text.startswith('golight'):
            self.terminal.go_lighter(val=0.5)

        else:
            self.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
            self.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')
            self.speak("I'm afraid I can't do that")
        self.numberOfCommandsUntilNow = self.numberOfCommandsUntilNow + 1

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass


class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()

        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', align='left', color='#808080')
        self.window.log('HAL9000 joined.', align='right', color='#808080')

        # Construct and initialize the agent for this simulation.
        self.agent = HAL9000(self.window)

        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.agent.on_input)
        self.window.events.user_command.connect(self.agent.on_command)

    def run(self):
        timer = vispy.app.Timer(interval=1.0)
        timer.connect(self.agent.update)
        timer.start()
        
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
