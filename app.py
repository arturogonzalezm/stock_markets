from backend.shares import setup_page_config, display_tabs, share_prices


def main():
    """
    Main function for the Streamlit app.
    :return: None
    """
    setup_page_config()
    tabs = display_tabs()
    share_prices(tabs[0])


if __name__ == "__main__":
    main()
