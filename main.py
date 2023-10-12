from flask import Flask, request, abort
from dotenv import load_dotenv
import os

load_dotenv()
acs_token=os.getenv('access_token')
handler=os.getenv('handler')

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ImageMessage,
    ReplyMessageRequest,
    StickerMessage,
    LocationMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token=acs_token)
handler = WebhookHandler(handler)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        input_text = event.message.text
        if input_text == '@Send Text':
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token = event.reply_token,
                    messages=[TextMessage(text = '111502532')]
                )
            )
        elif input_text == "@Send Image":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(originalContentUrl="https://i.pinimg.com/originals/f2/eb/37/f2eb37313587f7cc0dd858f496da49eb.jpg"
                                    ,previewImageUrl="https://i.pinimg.com/originals/f2/eb/37/f2eb37313587f7cc0dd858f496da49eb.jpg")
                    ]
                )
            )
        elif input_text == "@Send Sticker":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(
                        packageId='3',
                        stickerId='180'
                    )]
                )
            )
        elif input_text == "@Multiple Messages":
            Messages = [TextMessage(text="貧乳はステータスだ！"), TextMessage(text="希少価値だ！"),
                        ImageMessage(originalContentUrl="https://steamuserimages-a.akamaihd.net/ugc/242461372613402483/E7CBE731BE17B697B6FA760F6B51575A919AFD9A/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false"
                                    ,previewImageUrl="https://steamuserimages-a.akamaihd.net/ugc/242461372613402483/E7CBE731BE17B697B6FA760F6B51575A919AFD9A/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false")
                        ,StickerMessage(packageId='3',stickerId='184')
                        ]
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=Messages
                )
            )
        elif input_text == "@Send Location":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[LocationMessage(
                        title='こなたがここにすんだ',
                        address='埼玉縣幸手市',
                        latitude=36.0735998,
                        longitude=139.7404183
                    )]
                )
            )
        elif input_text == "@Quick Replies":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='Your Student Info',
                        quickReply=QuickReply(
                            items=[
                                QuickReplyItem(action=MessageAction(label='Name', text='陳玨嶧')),
                                QuickReplyItem(action=MessageAction(label='StudentID', text='111502532')),
                                QuickReplyItem(action=MessageAction(label='Your favorite fruit', text='Strawberry'))
                            ]
                        )
                    )]
                )
            )
        elif input_text == "Strawberry":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(originalContentUrl="https://cdn.donmai.us/original/a3/a2/a3a2157917b9219217bfbda643874771.png"
                                    ,previewImageUrl="https://cdn.donmai.us/original/a3/a2/a3a2157917b9219217bfbda643874771.png")
                    ]
                )
            )
        elif input_text == "Weeee":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(originalContentUrl="https://i.kym-cdn.com/photos/images/original/000/504/434/717.gif"
                                    ,previewImageUrl="https://i.kym-cdn.com/photos/images/original/000/504/434/717.gif")
                    ]
                )
            )
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

if __name__ == "__main__":
    app.run(host='0.0.0.0')