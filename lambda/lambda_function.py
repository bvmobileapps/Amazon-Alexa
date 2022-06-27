# -*- coding: utf-8 -*-

# This Alexa Skill plays the NAAB Smooth Jazz radio station.
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
STREAMS = [
  {
    "token": '1',
    "url": 'https://streaming.live365.com/a27716',
    "metadata": {
      "title": 'NAAB Smooth Jazz Radio',
      "subtitle": '',
      "art": {
        "sources": [
          {
            "contentDescription": 'NAAB Smooth Jazz radio station image',
            "url": 'https://www.blackvibes.com/images/bvc/212/45908-naab-smooth-jazz-nati.jpg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'example image',
            "url": '',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  }
]

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
        speech_output = "This command is not supported. Say Play, Stop, or Pause."
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(False)
                .response
            )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say play smooth jazz to start the radio."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
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

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say play smooth jazz to start the radio."
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

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