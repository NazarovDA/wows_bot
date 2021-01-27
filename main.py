import discord
from discord.ext import commands
from config import settings
import requests
import SQLITE

bot = commands.Bot(command_prefix = settings['prefix'])

'''
def create_request(section, subsection, requestedField, requestedFieldValue, extra=None, answerFieldValue=None):
    """
    :param extra:
    :param section: Верхний раздел API, к которому нужно обратиться
    :param subsection: Подраздел API, к которому нужно обратиться
    :param requestedField: Требуемое поле в API-запросе
    :param requestedFieldValue: Значение требуемого поля
    :param answerFieldValue: Значение, которые должны быть получены в ответ на запрос
    :return: Ссылка для запроса
    """

    if answerFieldValue is not None:
        fields = f'&fields={answerFieldValue.replace(", ", "%2c")}'
    else:
        fields = ""


    if extra is not None:
        extra_fields = f'&extra={extra.replace(", ", "%2c")}'   
    else:
        extra_fields = ""



    request = f"https://api.worldofwarships.ru/wows/{section}/{subsection}/" \
              f"?application_id={settings['app_id']}&{requestedField}={requestedFieldValue}{extra}{fields}"

    # https://api.worldofwarships.ru/wows/clans/info/?application_id=4806e69507777a7881a524bcd5e94d6f&clan_id=430054&extra=members%2C+creator_name&fields=member_ids

    return request
'''


async def clanStatsPerDay(clan_id):
    request = requests.get(f"https://api.worldofwarships.ru/wows/clans/info/?application_id={settings['app_id']}"
                           f"f&clan_id={clan_id}&fields=member_ids").json()


@bot.command()
async def add(ctx):
    author = ctx.message.author
    message = ctx.message
    request = f"https://api.worldofwarships.ru/wows/account/list/?application_id={settings['app_id']}" \
              f"&search={message.content[5:]}&fields=account_id"
    answer = requests.get(request).json()
    sqlite.add(
        inGameNickname = message.content[5:],
        discordNickname = author,
        playerId = answer['data'][0]['account_id']
    )
    if answer["status"] == "error":
        await ctx.send(f"Что-то пошло не так. Ошибка:{answer['error']}")
    else:
        await ctx.send(f"Добавил {author.mention} в базу данных для рассылки")


@bot.command()
async def hi(ctx):
    await ctx.send('hello')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


sqlite = SQLITE.SQLiter()
bot.run(settings['token'])
