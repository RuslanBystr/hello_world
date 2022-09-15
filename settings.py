import datetime
import json

VOICE_ID = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\TokenEnums\\RHVoice\\Volodymyr"

NAME = "Діма"

ALIAS = [
    "діма",
    "дімон",
    "дмитро",
    "дімич",
    "дім"
]

EXEC_CMDS = {
    "wiki":         "CmdFunc._search_in_wiki()",
    "new_txt":      "CmdFunc._new_txt()",
    "write":        "CmdFunc._write()",
    "now_time":     "CmdFunc._now_time()",
    "calculate":    "CmdFunc._calculate()",
    "weather":      "CmdFunc._now_weather()",
    "news":         "CmdFunc._news()",
    "get_dolar":    "CmdFunc._get_dolar()",
    "get_euro":     "CmdFunc._get_euro()",
    "speak_faster": "CmdFunc._speak_faster()",
    "speak_slower": "CmdFunc._speak_slower()",
    "exit":         "CmdFunc._exit()"
}

REC_LANG = "uk-UK"

NOW_TIME = datetime.datetime.now()

