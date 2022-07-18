# -*- coding: utf-8 -*-

# This Alexa Skill plays a radio station from the specified URL.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective, ClearQueueDirective, ClearBehavior)

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Audio stream metadata
# The stream URL needs a valid SSL certificate and needs to start with 'https' and not 'http' otherwise it will not play.
STREAMS = [
  {
    "token": '1',
    "url": 'https://streaming.live365.com/a27716',
    "metadata": {
      "title": 'Radio Station Name Goes Here',
      "subtitle": '',
      "art": {
        "sources": [
          {
            "contentDescription": 'Radio Station Logo',
            "url": 'https://www.blackvibes.com/images/bvc/212/45908-naab-smooth-jazz-nati.jpg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": '',
            "url": '',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  }
]

# Strings used to reply to user input. Modify them here if necessary.
STR_HELP_INTENT = ("You can say play {} to start the radio.".format(STREAMS[0]["metadata"]["title"]))
STR_UNSUPPORTED_COMMAND = ("This command is not supported. Say Play, Stop, or Pause.")
STR_FALLBACK_INTENT = ("Hmm, I'm not sure. You can say play {} to start the radio.".format(STREAMS[0]["metadata"]["title"]))
STR_EXCEPTION = ("Sorry, I had trouble doing what you asked. Please try again.")

# Automatically plays the radio station when activity is launched without intent.
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .speak("Starting {}".format(stream["metadata"]["title"]))
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )

# Used to start the radio station. Right now it is set up to only handle one radio station.
class PlayRadioStationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlayRadioStationIntent")(handler_input)
        
    def handle(self, handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .speak("Starting {}".format(stream["metadata"]["title"]))
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )

# Handler for when the user says "resume" or anything along those lines.
class ResumeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.ResumeIntent")(handler_input)
        
    def handle(self, handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )

# This handler handles all the required audio player intents which are not supported by the skill yet. 
class UnhandledFeaturesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.LoopOnIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.NextIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.PreviousIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.RepeatIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.ShuffleOnIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.StartOverIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.ShuffleOffIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.LoopOffIntent")(handler_input)
                )
    
    def handle(self, handler_input):
        speak_output = STR_UNSUPPORTED_COMMAND
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
            )

# Handler for Help Intent.
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = STR_HELP_INTENT

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Single handler for Cancel and Stop Intent.
class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
                or ask_utils.is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ALL)
                        )
                    .add_directive(StopDirective())
                    .set_should_end_session(True)
                    .response
                )

# Single handler for Fallback Intent.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speak_output = STR_FALLBACK_INTENT

        return handler_input.response_builder.speak(speak_output).response

# Handler for Session End.
class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = STR_EXCEPTION

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PlayRadioStationHandler())
sb.add_request_handler(ResumeIntentHandler())
sb.add_request_handler(UnhandledFeaturesIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
