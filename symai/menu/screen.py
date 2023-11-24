import sys
import webbrowser
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.shortcuts import yes_no_dialog, input_dialog, button_dialog
from prompt_toolkit.styles import Style
from ..misc.console import ConsoleStyle


def show_splash_screen(print: callable = print_formatted_text):
    print('\n\n')
    print('- '*42)
    print('=='*41 + '=')
    print(r'''
      ____|        |                      _)  |              \    _ _|
      __|  \ \  /  __|   _ \  __ \    __|  |  __|  |   |    _ \     |
      |     `  <   |     __/  |   | \__ \  |  |    |   |   ___ \    |
     _____| _/\_\ \__| \___| _|  _| ____/ _| \__| \__, | _/    _\ ___|
                                                  ____/
    ''')
    print('- '*17 + ' ExtensityAI ' + ' -'*18  + '\n')


def show_info_message(print: callable = print_formatted_text):
    print('Welcome to SymbolicAI!' + '\n')
    print('SymbolicAI is an open-source Python project for building AI-powered applications\nand assistants.')
    print('We utilize the power of large language models and the latest research in AI.' + '\n')
    print('SymbolicAI is backed by ExtensityAI, an open-source non-profit organization. We are\ncommitted to open research, the democratization of AI tools and much more ...' + '\n')

    print('... and we also like peanut butter and jelly sandwiches, and cookies.' + '\n\n')
    print('If you like what we are doing please help us achieve our mission!')
    print('More information is available at https://www.extensity.ai' + '\n')


def show_separator(print: callable = print_formatted_text):
    print('- '*42 + '\n')


def is_openai_api_model(key: str):
    return 'gpt' in key or 'text' in key


def show_main_setup_menu(session: PromptSession = None):
    if session is None:
        session = PromptSession()

    # Step 1: Accept terms and services
    agreed = yes_no_dialog(
        title="Terms of Service",
        text="Do you accept the terms of service and privacy policy?",
    ).run()
    if not agreed:
        print_formatted_text("You need to accept the terms of services to continue.")
        sys.exit(0)

    # Step 2: Enter OpenAI Key

    # Step 2.1: Select model
    nesy_engine_model = input_dialog(
        title="Select Model",
        text="Please select a OpenAI model (https://platform.openai.com/docs/models) or a custom neuro-symbolic model:",
        default="gpt-3.5-turbo"
    ).run()

    # Step 2.2: Enter API key
    if is_openai_api_model(nesy_engine_model):
        nesy_engine_api_key = input_dialog(
            title="OpenAI API Key",
            text="Please enter your OpenAI API Key (https://platform.openai.com/api-keys):",

        ).run()
        if not nesy_engine_api_key:
            with ConsoleStyle('warn') as console:
                console.print("No API key or custom model ID provided. The framework will not work without it.")
    else:
        nesy_engine_api_key = input_dialog(
            title="[Optional] Neuro-Symbolic Model API Key",
            text="Please enter your Neuro-Symbolic Model API Key if applicable:",
        ).run()

    # Step 2.3: Enter Embedding Engine API Key is_openai_api_model(nesy_engine_model)
    if is_openai_api_model(nesy_engine_model):
        embedding_engine_api_key = nesy_engine_api_key
    else:
        embedding_engine_api_key = input_dialog(
            title="[Optional] Embedding Engine API Key",
            text="Please enter your Embedding Engine API Key if applicable:",
        ).run()

    # Ask for optional settings yes/no
    continue_optional_settings = yes_no_dialog(
        title="Optional Settings",
        text="Do you want to configure optional settings?",
    ).run()

    embedding_model = ''
    symbolic_engine_api_key = ''
    symbolic_engine_model = ''
    imagerendering_engine_api_key = ''
    vision_engine_model = ''
    search_engine_api_key = ''
    search_engine_model = ''
    ocr_engine_api_key = ''
    speech_to_text_engine_model = ''
    text_to_speech_engine_model = ''
    text_to_speech_engine_voice = ''
    indexing_engine_api_key = ''
    indexing_engine_environment = ''
    caption_engine_environment = ''

    if continue_optional_settings:
        # Step 2.4: Enter Embedding Model
        embedding_model = input_dialog(
            title="[Optional] Embedding Model",
            text="Please enter a embedding model (https://huggingface.co/models?pipeline_tag=text2text-generation) if applicable:",
            default="text-embedding-ada-002"
        ).run()

        # Step 2.5: Symbolic Engine API Key
        symbolic_engine_api_key = input_dialog(
            title="[Optional] Symbolic Engine API Key",
            text="Please enter your Symbolic Engine API Key if applicable:",
        ).run()

        if symbolic_engine_api_key:
            # Step 2.6: Symbolic Engine Model
            symbolic_engine_model = input_dialog(
                title="[Optional] Symbolic Engine Model",
                text="Please enter your Symbolic Engine Model if applicable:",
                default="wolframalpha"
            ).run()

        # Step 2.7: Enter Imagerendering engine api key
        if is_openai_api_model(nesy_engine_model):
            imagerendering_engine_api_key = nesy_engine_api_key
        else:
            imagerendering_engine_api_key = input_dialog(
                title="[Optional] Image Rendering Engine API Key",
                text="Please enter your Image Rendering Engine API Key if applicable:",
            ).run()

        # Step 2.8: Enter Vision Engine Model
        vision_engine_model = input_dialog(
            title="[Optional] Vision Engine Model",
            text="Please enter your Vision Engine Model if applicable:",
            default="openai/clip-vit-base-patch32"
        ).run()

        # Step 2.9: Enter Search Engine API Key
        search_engine_api_key = input_dialog(
            title="[Optional] Search Engine API Key",
            text="Please enter your Search Engine API Key if applicable:",
        ).run()

        if search_engine_api_key:
            # Step 2.10: Enter Search Engine Model
            search_engine_model = input_dialog(
                title="[Optional] Search Engine Model",
                text="Please enter your Search Engine Model if applicable:",
                default="google",
            ).run()

        # Step 2.11: Enter OCR Engine API Key
        ocr_engine_api_key = input_dialog(
            title="[Optional] OCR Engine API Key",
            text="Please enter your OCR Engine API Key if applicable:",
        ).run()

        # Step 2.12: Enter Speech-to-Text Engine Model
        speech_to_text_engine_model = input_dialog(
            title="[Optional] Speech-to-Text Engine Model",
            text="Please enter your Speech-to-Text Engine Model if applicable:",
            default="base"
        ).run()

        # Step 2.13: Enter Text-to-Speech Engine Model
        text_to_speech_engine_model = input_dialog(
            title="[Optional] Text-to-Speech Engine Model",
            text="Please enter your Text-to-Speech Engine Model if applicable:",
            default="tts-1"
        ).run()

        # Step 2.14: Enter Text-to-Speech Engine Voice
        text_to_speech_engine_voice = input_dialog(
            title="[Optional] Text-to-Speech Engine Voice",
            text="Please enter your Text-to-Speech Engine Voice if applicable:",
            default="echo"
        ).run()

        # Step 2.15: Enter Indexing Engine API Key
        indexing_engine_api_key = input_dialog(
            title="[Optional] Indexing Engine API Key",
            text="Please enter your Indexing Engine API Key if applicable:",
        ).run()

        # Step 2.16: Enter Indexing Engine Environment
        indexing_engine_environment = ''
        if indexing_engine_api_key:
            indexing_engine_environment = input_dialog(
                title="[Optional] Indexing Engine Environment",
                text="Please enter your Indexing Engine Environment if applicable:",
                default="us-west1-gcp"
            ).run()

        # Step 2.17: Enter Caption Engine Environment
        caption_engine_environment = input_dialog(
            title="[Optional] Caption Engine Environment",
            text="Please enter your Caption Engine Environment if applicable:",
            default="blip2_opt/pretrain_opt2.7b"
        ).run()

    # Step 3: Enable/Disable community support and data sharing
    support_community = yes_no_dialog(
        title="Community Support and Data Sharing",
        text="Enable community support and data sharing?",
    ).run()
    if not support_community:
        with ConsoleStyle('info') as console:
            msg = 'To support us improve our framework consider enabling this setting in the future. By doing so you  not only improve your own user experience but help us deliver new and exciting solutions in the future. Your data is uploaded to our research servers, and helps us develop on-premise solutions and the overall SymbolicAI experience. We do not sell or monetize your data otherwise. We thank you very much for supporting the research community and helping us thrive together! If you wish to update this option go to your .symai config situated in your home directory or set the environment variable `SUPPORT_COMMUNITY` to `True`.'
            console.print(msg)

    # Step 4: Donate to the open-source collective
    donation_result = button_dialog(
        title="Support ExtensityAI @ Open-Source Collective",
        text="Would you like to donate to ExtensityAI at the open-source collective?",
        buttons=[
            ('Yes', True),
            ('No', False)
        ],
    ).run()
    if donation_result:
        # open link to the open collective donation page in the browser
        webbrowser.open('https://opencollective.com/symbolicai')
        with ConsoleStyle('success') as console:
            msg = 'We are so happy that you consider to support us! Your contribution helps feed our starving cookie monster researcher staff. If you wish to further support us in the future, you can visit us at our open collective page https://opencollective.com/symbolicai and keep track of our expenses and donations. We thank you very much for your support!'
            console.print(msg)
    else:
        with ConsoleStyle('alert') as console:
            msg = 'Being an open-source non-profit organization we rely on donations to keep our servers running and to support our researchers. If you wish that we can thrive together please consider donating to our open collective. Without your support we cannot continue our mission, since also peanuts and jelly sandwiches are not free, or even cookies for that matter. You can donate at https://opencollective.com/symbolicai and keep track of our expenses and donations. We thank you very much for your support!'
            console.print(msg)


    # Process the setup results
    settings = {
        'terms_agreed': agreed,
        'nesy_engine_model': nesy_engine_model if nesy_engine_model else '',
        'nesy_engine_api_key': nesy_engine_api_key,
        'symbolic_engine_api_key': symbolic_engine_api_key,
        'symbolic_engine_model': symbolic_engine_model,
        'support_community': support_community,
        'donated': donation_result,
        'embedding_engine_api_key': embedding_engine_api_key if embedding_engine_api_key else '',
        'embedding_model': embedding_model,
        'imagerendering_engine_api_key': imagerendering_engine_api_key if imagerendering_engine_api_key else '',
        'vision_engine_model': vision_engine_model,
        'search_engine_api_key': search_engine_api_key,
        'search_engine_model': search_engine_model,
        'ocr_engine_api_key': ocr_engine_api_key,
        'speech_to_text_engine_model': speech_to_text_engine_model,
        'text_to_speech_engine_model': text_to_speech_engine_model,
        'text_to_speech_engine_voice': text_to_speech_engine_voice,
        'indexing_engine_api_key': indexing_engine_api_key,
        'indexing_engine_environment': indexing_engine_environment,
        'caption_engine_environment': caption_engine_environment
    }

    return settings


def show_intro_menu():
    with ConsoleStyle('extensity') as console:
        show_splash_screen(print=console.print)
    with ConsoleStyle('text') as console:
        show_info_message(print=console.print)
    with ConsoleStyle('extensity') as console:
        show_separator(print=console.print)


def show_menu(session: PromptSession = None):
    show_intro_menu()
    return show_main_setup_menu(session=session)


if __name__ == '__main__':
    show_menu()