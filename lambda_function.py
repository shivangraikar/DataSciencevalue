import json
from save_request import to_s3
from scorer import calculate_score
from pre_treatment import treat_input
from probability import calc_proba


def lambda_handler(event, context):
    # We are doing some prints for CloudWatch logging purposes
    print(event)

    if event['body-json'] == {}:
        event = event['params']['querystring']
    else:
        event = event['body-json']
        event = {x.split('=')[0]: x.split('=')[1] for x in event.split("&")}

    treated_event = treat_input(event)
    print(treated_event)

    score = calculate_score(treated_event)
    proba = calc_proba(score)
    treated_event = {'input_data': treated_event,
                     'score': score,
                     'proba': proba}

    print(score)
    # build response
    r = {"score": score, "proba": proba,
         "message": "The probability of someone \
    with this score earn more than USD 100.000/year is {}.".format(proba)}
    print(r)
    to_s3(treated_event)

    status_code = 200

    response = {
        "isBase64Encoded": False,
        "headers": {"Content-Type": "application/json"},
        "statusCode": status_code,
        "body": json.dumps(r)
    }

    return response
