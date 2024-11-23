import telebot
from io import BytesIO
from PIL import Image
from ollama import generate

BOT_TOKEN = '7699678198:AAF8JrKWJgFW7vQVIM3nMdE2TbvYXfMAVSY'

bot = telebot.TeleBot(BOT_TOKEN)


def reset(message,history):
    return []
    # bot.reply_to(message,"Knowladge Restart")

@bot.message_handler(commands=['hello','hi'])
def send_welcome(message):
    # bot.reply_to(message, "Knowladge Restart")
    bot.reply_to(message, "Hi I'm Zoro your AI Assistant. how can i help you?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(message)
    response_bot = message.text
    bot.reply_to(message,response_bot )



def process_image(image_file):
    """Convert the image to bytes."""
    with Image.open(image_file) as img:
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()

def generate_photo_analysis(image_bytes):
    """Generate a photo analysis response using the LLava model."""
    prompt = """
    You are a professional photo analyst.  
    Analyze the photo and provide only **useful observations** for each of the following points:
    
    **Main Objects**: Identify the key objects, people, or animals, including relevant colors or textures.  
    **Key Takeaway or Story**: Provide any deeper narrative or meaning the image conveys.
    
    If the photo conveys emotion, describe it.  
    Be concise. Avoid unnecessary details or repetition. Provide only what is essential and insightful.
    Make it simple.
    """

    # Accumulate the streamed responses
    full_response = "".join(
        response['response'] for response in generate(
            model='llava:13b',
            prompt=prompt,
            images=[image_bytes],
            stream=True
        )
    )
    return full_response








@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("/home/hendry/telegram/{}".format(file_info.file_path), 'wb') as new_file:
        new_file.write(downloaded_file)
    image_file = "/home/hendry/telegram/{}".format(file_info.file_path)


    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
    
    image_bytes = process_image(image_file)
    response = generate_photo_analysis(image_bytes)


    bot.reply_to(message,response)

    

bot.infinity_polling()