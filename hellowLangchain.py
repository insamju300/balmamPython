# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os 

load_dotenv()

print(f"[API KEY]\n{os.environ['OPENAI_API_KEY']}")

## 참고할 것 https://github.com/nomadcoders/fullstack-gpt