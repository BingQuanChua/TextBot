import discord
from discord.ext import commands
from pathlib import Path
from decouple import config

#textblob
from textblob import TextBlob

# spacy and friends
import spacy
from spacy import displacy
from spacytextblob.spacytextblob import SpacyTextBlob

# convert svg to other formats
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM



# client = discord.Client()
client = commands.Bot(command_prefix=';')

# list of responses
emotion = [':grinning:', ':slight_smile:', ':no_mouth:', ':slight_frown:', ':frowning2:']
score_metre = [':red_square:', ':orange_square:', ':yellow_square:', ':green_square:', ':green_square:']
background = [':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:']

# spacy nlp set language
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

# start of the bot
@client.event
async def on_ready():
    print('TextBot is online!')

# bot commands
@client.command()
async def hi(context):
    await context.channel.send('ayy')
    await context.channel.send(f'latency: {round(client.latency*1000)} ms')

@client.command(aliases=['a'])
async def analyse(ctx, *, message):
    blob = TextBlob(message)
    stats = discord.Embed()
    stats.title='Message Stats :speech_balloon:'
    stats.description = f'Message: ```{message}```{getStats(blob.sentiment.polarity, blob.sentiment.subjectivity)}'
    await ctx.channel.send(embed=stats)

def getStats(polarity, subjectivity):
    polarity = round(polarity, 2)
    subjectivity = round(subjectivity, 2)
    if polarity >= 0.7:
        emoji = emotion[0]
        metre = ''.join(score_metre)
    elif polarity > 0:
        emoji = emotion[1]
        metre = ''.join(score_metre[0:4]) + ''.join(background[0:1])
    elif polarity <= -0.7:
        emoji = emotion[4]
        metre = ''.join(score_metre[0:1]) + ''.join(background[0:4])
    elif polarity < 0:
        emoji = emotion[3]
        metre = ''.join(score_metre[0:2]) + ''.join(background[0:3])
    else:
        emoji = emotion[2]
        metre = ''.join(score_metre[0:3]) + ''.join(background[0:2])
    return f'\nOverall: {emoji} \n\nPolarity: {metre} {polarity} \n\nSubjectivity: {subjectivity}'

@client.command(aliases=['at'])
async def analyse_text(ctx, *, message):
    await ctx.channel.send('nice')

@client.command(aliases=['ad'])
async def analyse_dependency(ctx, *, message):
    ### use displacy to render dependency
    doc = nlp(message)
    svg = displacy.render(doc, style='dep', jupyter=False)

    try:
        ### output as png
        output_path = Path('dep.svg')
        output_path.open('w', encoding='utf-8').write(svg)
        #await ctx.channel.send(file=discord.File('dep.svg')) 

        ### convert svg to png
        drawing = svg2rlg('dep.svg')
        renderPM.drawToFile(drawing, 'dep.png', fmt='PNG')
        #await ctx.channel.send(file=discord.File('dep.png')) 

        ### sending embed result
        m = discord.Embed()
        m.title='Message Dependency :chart_with_upwards_trend:'
        m.description = f'Message: ```{message}``` \nResult:'
        m.set_image(url='attachment://dep.png')
        await ctx.channel.send(file=discord.File('dep.png'), embed=m)

    except Exception as ex:
        print(ex)
        await ctx.channel.send('Sorry. There was an error.')

@client.command(aliases=['ner'])
async def named_entity_recognition(ctx, *, message):
    ### use displacy to render dependency
    doc = nlp(message)
    d = dict()
    for word in doc.ents:
        d.setdefault(word.label_, [])
        d[word.label_].append(word.text)

    m = discord.Embed()
    m.title='Named-Entity Recognition :label:'
    desc = f'Message: ```{message}``` \nResult:\n'
    for k, v in d.items():
        desc += ('`' + k + '` : ')
        for i in v:
            desc += (i + ' ')
        desc += "\n"

    m.description = desc
    await ctx.channel.send(embed=m)

@client.command(aliases=['e'])
async def explain(ctx, *, message):
    e = spacy.explain(message.upper())
    if e != None:
        m = discord.Embed()
        m.title = 'Explanation :book:'
        m.description = f'Tag/Label: ```{message}``` \nExplanation: ```{e}```'
        await ctx.channel.send(embed=m)
    else:
        m = discord.Embed()
        m.description = 'There is no explaination for this Tag/Label.\n**Tags and Labels must be case-sensitive.'
        await ctx.channel.send(embed=m)

# help message
client.remove_command('help') # remove default help message

@client.command(aliases=['h'])
async def help(ctx):
    m = discord.Embed()
    m.title = 'Help :scroll:'
    m.description = 'Commands currently available to TextBot.'
    m.add_field(name='Analyse a text', value='```;[a|analyse|a] [message]``` Analyse the given sentence using sentiment analysis.\n\n+ive :grinning:-:slight_smile:-:no_mouth:-:slight_frown:-:frowning2: -ive', inline=False)
    m.add_field(name='Visualize Dependency', value='```;[ad|analyse_dependency] [message]``` Render a dependency graph for the given sentence.', inline=False)
    m.add_field(name='Named Entity Recognition ', value='```;[ner|named_entity_recognition] [message]``` Detect and classify text into predefined categories or real world object entities.', inline=False)
    m.add_field(name='Explain tag or label', value='```;[e|explain] [tag|label]``` Explain a tag or label from spaCy.', inline=False)
    # m.add_field(name='```;[analyse_text|at] [textfile]```', value='Upload a text file for sentiment analysis.', inline=False)
    m.set_footer(text='Hackerspace Hackathon 2021')
    await ctx.channel.send(embed=m)

# error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print('Command not found')

@analyse.error
@analyse_dependency.error
@named_entity_recognition.error
@explain.error
async def analyse_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        m = discord.Embed(description='Command incomplete! \nPlease refer to [help](https://www.youtube.com/watch?v=dQw4w9WgXcQ).')
        await ctx.channel.send(embed=m)
        

# run bot
client.run(config('TOKEN'))
#client.run(environ.get('TOKEN'))