**🎯 Objective of Project**
---

The results of the Municipal Elections, Parliamentary Elections, and Presidential Elections were extracted from the website https://acikveri.ysk.gov.tr/secim-sonuc-istatistik/secim-sonuc using Selenium. Then, a program was developed using Streamlit to conduct question-and-answer sessions with an LLM that possesses this information.

**💻 Technologies Used in the Project**
---

• Data Validation: Pydantic-Settings

• ORM: (Async) SqlAlchemy

• Web Automation: Selenium

• Migration Operations: Alembic

• Interface: Streamlit

• Platform Running the LLM: Ollama

• LLM Model Name: kimi-k2.5:cloud

• Log Monitoring: Logging

• Agent Management: Langchain

**🗂️ Files in the Langchain_Sql_Secim_Portali Folder Properties**
---

• langchain_sql_configuration.py: This file uses the tools associated with the SQLDatabaseToolkit class in Langchain so that the Agent can answer user questions, and the agent also has short-term memory.

• Main.py: Main operations are performed in this file.

• Models.py: The existing tables in the database are located here.

• my_py_settings.py: Data validation operations with Pydantic are performed on this page.

• sql_alchemy_operations.py: Database operations are performed here.

• streamlit_operations.py: Message adding operations related to Streamlit are performed here.

**🗂️ Properties of Files in the Selenium_Web_Automation Folder**
---

• Conversion_module.py: This file is used to convert string data to another format during data retrieval with Selenium.

• Member_of_Parliament_Districts_special_code.py: A special code was written to retrieve districts in parliamentary elections.

• Models.py: Database tables are located here.

• Pydantic_Page.py: Data validation operations with Pydantic are performed on this page.

• selenium_operations.py: This page is used as a Main file when retrieving data in Selenium.

• selenium_helper_functions.py: Commands such as waiting, clicking, or page loading in Selenium are located here.

• sql_alchemy_operations.py: Record insertion into the database, value updating, or Select operations are performed here.

• Turkey_province_candidate_data_retrieval_code.py: Created to retrieve the number of votes and vote percentages received by candidates in cities during the Presidential Elections.

• Turkey_districts_candidate_data_retrieval.py: • Created to retrieve the number of votes and vote percentages received by candidates in districts during Presidential Elections.

• Turkiye_ilceler_veri_cekme_kodu.py: Created to retrieve the number of votes and vote percentages of parties in districts during General Parliamentary Elections and Mayoral Elections.

• Turkiye_iller_veri_cekme_kodu.py: Created to retrieve the number of votes and vote percentages of parties in cities during General Parliamentary Elections and Mayoral Elections.

• Selenium_Secim_Portali_Projesi_Grafiği.png: This file shows how the processes are carried out with a short graphic. 

**📌 Additional Explanation**
---
In addition to the vote count and vote percentages for parties and candidates, data such as the number of registered voters, valid votes, and the number of voters who cast their votes in cities and districts are also recorded in the database.
Other Information



⚠️ This repository is designed to demonstrate the project's architecture and coding standards. Due to security and privacy reasons, some API configurations and private keys have not been included; therefore, the project is not in "plug-and-play" mode, but is an example of a technical portfolio.
