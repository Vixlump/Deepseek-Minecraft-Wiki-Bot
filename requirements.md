You need to install the following for this bot to work.
```
pip3 install requests
pip3 install beautifulsoup4
pip3 install ollama
pip3 install numpy
pip3 install scikit-learn
```

also download ollama itself: https://ollama.com/download

if you are on windows you need to add ollama to the PATH manually by entering "environment variables" and adding "C:\Users\<YourUsername>\AppData\Local\Programs\Ollama" to "PATH"

Install embedder manually
```
ollama pull nomic-embed-text
```
Install deepseek distilled with the following command
```
ollama run deepseek-r1:14b
```
setup project with:
```
python main.py --setup
```
run bot with
```
python main.py --chat
```