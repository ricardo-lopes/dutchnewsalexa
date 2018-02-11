from __future__ import print_function
import DutchNewsFeed


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    speech_output = "<speak>Dutch news dot nl <break time=\"2s\"/> Please ask what's new</speak>"
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(speech_output, None, should_end_session))


def handle_session_end_request():
    speech_output = "<speak>Bye. For more go to dutch news dot nl</speak>"
    should_end_session = True
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session))


def get_dutch_news(intent, session):
    session_attributes = get_session_attributes(session)
    response = "<speak>Today on dutch news dot nl <break time=\"1s\"/>"
    item = session_attributes['item']
    response += DutchNewsFeed.get_feed_title(item)
    response += get_detail_question()
    response += "</speak>"
    speech_output = response
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(speech_output, None, should_end_session))


def get_dutch_news_item_details(intent, session):
    session_attributes = get_session_attributes(session)
    item = session['attributes']['item']
    response = "<speak>"
    response += DutchNewsFeed.scrape_feed_item(item)
    response += get_next_title(intent, session)
    response += "</speak>"
    speech_output = response
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(speech_output, None, should_end_session))


def get_next_title(intent, session):
    item = session['attributes']['item'] + 1
    response = "Next on dutch news dot nl <break time=\"1s\"/>"
    response += DutchNewsFeed.get_feed_title(item)
    response += get_detail_question()
    return response


def get_session_attributes(session):
    if "item" in session.get('attributes', {}):
        item = session['attributes']['item']
        if item < 9:
            item = item + 1
        else:
            item = 0
        return {"item": item}
    else:
        return {"item": 0}


def get_detail_question():
    return "Do you want to hear more on this item?"


# --------------- Specific Events ------------------

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "NewItemsIntent":
        return get_dutch_news(intent, session)
    if intent_name == "NoDetailsIntent":
        return get_dutch_news(intent, session)
    if intent_name == "YesDetailsIntent":
        return get_dutch_news_item_details(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# --------------- Generic Events ------------------

def on_session_started(session_started_request, session):
    print(
        "on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_welcome_response()


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
