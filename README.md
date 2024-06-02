# AutoSTTop
A Speech-To-Text program in different languages, using [MMS-1b-all Automatic-Speech-Recognition](https://huggingface.co/facebook/mms-1b-all) model built by Facebook.

Made with FastAPI for Backend and Streamlit for Frontend. 


### Supported Languages
See the supported ones in the dictionary of `backend/lang_options.py`

If you want to add one, notice if it is available  (in the ASR label) [here](https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html) and add it's name and respective code. 

### HOW TO USE 
1. Install all the dependencies

        pip install -r requirements.txt

2. Go to the Backend folder - `cd backend` - and run: 

        python stt.py


3. Locate in the root path - `cd ..` - and then run the frontend: 

        streamlit run app.py