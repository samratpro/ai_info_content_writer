from customtkinter import *
from models import Postdata, Session


class SettingsPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.default_website_name = "https://website.com"
        self.default_username = "admin"
        self.default_app_pass = "xxxx xxxx xxxx xxxx"
        self.default_category_name = "review"
        self.default_chatgpt_api = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.default_chatgpt_model = 'model name'
        self.default_deepseek_api = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.default_deepseek_model = 'model name'
        self.default_gemni_api = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.default_gemni_model = 'model name'
        self.default_api_select = "ChatGPT"
        self.default_title_prompt = '''Write an SEO title about this keyword within 55 characters. The keyword must be included directly in the title keyword: ((keyword))
rules:
1. Never mention year
2. Must be within 55 characters
3. Must be clickbait'''
        self.default_intro_prompt = """Write a compelling blog post introduction about the keyword: ((keyword)) 
The introduction should begin with technical terms related to the topic, avoiding casual phrases like "Are you...". The keyword should be naturally included throughout the introduction. Do not provide a direct solution in the intro. 
The final sentence should intrigue readers to continue reading the full article. Aim for a length of approximately 120 words. """
        self.default_h2_prompt = """Write an sub title on this keyword, this title will insert before a production comparison list : ((keyword))
rules:
1. Must be interesting
2. Never directly place keyword"""
        self.default_h2_brief_prompt = """Generate a concise summary (not an introduction) before the main article, around 80 words.  
Ensure the summary includes the keyword: "<<keyword>>".  
Avoid phrases like "In this article" or "We will explore".  
Keep it engaging, informative, and to the point. """
        self.default_outline_prompt = """Generate an outline for a buying guide for the keyword: ((keyword)) [What to consider before purchasing a product].
The outline consists of multiple H2 sections with key subtopics underneath.
Instructions:
1. Only provide an outline—no explanations, answers, or unnecessary text.
2. The outline should have 5-6 H2 sections with concise subtopics below each.
3. Do not include headings like "Overview," "Introduction," or "Conclusion."
4. The outline will be placed at the bottom of a product review article (not a standalone article).
Follow this exact structure:
<h2>[Heading]</h2>
  - [Subtopic]
  - [Subtopic]
  - [Subtopic]
<h2>[Heading]</h2>
  - [Subtopic]
  - [Subtopic]
  - [Subtopic]
  <!-- Add more subtopics if necessary -->"""
        self.default_paragraph_prompt = """Write a buying guide paragraph explaining why it is important to consider Connectivity and Expansion before purchasing a ((keyword)). Ensure all sentences are meaningful and written in a natural, native style.
**Instructions:**  
1. **Do not** start the paragraph with the heading name.  
2. **Must avoid** using the phrases:  
   - "when considering"  
   - "choosing"  
   - "selecting"  
   - "looking"  
   - "seeking"  
   - "searching"
   - "purchasing"
   - "buying"
   - "purchasing"
   - "buying"
   - "Connectivity" 
   - "Expansion" 
   - "((keyword)) " (do not include this in output).  
   - "what to consider before purchase a product" (do not include this in output).
   - The exact words: **"Connectivity" and "Expansion"**  
3. **Start directly with an informative fact** instead of general advice.  
4. **Maintain a structured format** covering all given topics.  
5. Enhance readability with <p>, <strong>, <ul>, and <table> tags where appropriate. Use a <table> only when presenting structured comparisons, multiple data rows, pros vs. cons, or one topic vs. another. Avoid adding tables for simple lists or single-topic explanations.
6. Omit ```html``` label

**Details:**  
- **Keyword (for reference only, do not include in the output):** ((keyword))
- **Paragraph Heading:** ((heading))
- **Topics to Cover:**  
((topic_to_cover))"""
        self.default_faq_h2 = "FAQ's"
        self.default_faq_question_prompt = """Topic: ((keyword))
Write 5 related questions on this topic
1.
"""
        self.default_faq_ans_prompt = """Write a short answer to this question within 2 sentence ((question))"""
        self.default_conclusion_h2 = "Conclusion"
        self.default_conclusion_prompt = """keyword: ((keyword)) Write an web article bottom summary and length approx. 60 words"""

        # Create a session to interact with the database
        session = Session()
        self.data_check = session.query(Postdata).filter_by(id=1).first()
        print(self.data_check)

        if self.data_check is None:
            default_data = Postdata(
                website_name=self.default_website_name,
                username=self.default_username,
                app_pass=self.default_app_pass,
                category_name=self.default_category_name,
                chatgpt_api=self.default_chatgpt_api,
                chatgpt_model=self.default_chatgpt_model,
                deepseek_api=self.default_deepseek_api,
                deepseek_model=self.default_deepseek_model,
                gemni_api=self.default_gemni_api,
                gemni_model=self.default_gemni_model,
                api_select=self.default_api_select,
                title_prompt=self.default_title_prompt,
                intro_prompt=self.default_intro_prompt,
                h2_prompt=self.default_h2_prompt,
                h2_brief_prompt=self.default_h2_brief_prompt,
                outline_prompt=self.default_outline_prompt,
                paragraph_prompt=self.default_paragraph_prompt,
                faq_h2=self.default_faq_h2,
                faq_question_prompt=self.default_faq_question_prompt,
                faq_ans_prompt=self.default_faq_ans_prompt,
                conclusion_h2=self.default_conclusion_h2,
                conclusion_prompt=self.default_conclusion_prompt
            )
            session.add(default_data)
            session.commit()
            self.data_check = default_data

        print("Done")

        # Title Label
        self.label = CTkLabel(self, text="Settings Page", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create a scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self, width=500, height=400, border_width=1)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Create Labels and Entries for each field inside the scrollable frame
        self.fields = [
            ("Website Name", "website_name_entry", "website_name"),
            ("Username", "username_entry", "username"),
            ("Application Pass", "app_pass_entry", "app_pass"),
            ("Category Name", "category_name_entry", "category_name"),
            ("ChatGPT API", "chatgpt_api_entry", "chatgpt_api"),
            ("ChatGPT model", "chatgpt_model_entry", "chatgpt_model"),
            ("DeepSeek API", "deepseek_api_entry", "deepseek_api"),
            ("DeepSeek model", "deepseek_model_entry", "deepseek_model"),
            ("Gemni API", "gemni_api_entry", "gemni_api"),
            ("Gemni model", "gemni_model_entry", "gemni_model"),
            ("Select API", "api_select_entry", "api_select"),
            ("Title Prompt", "title_prompt_entry", "title_prompt"),
            ("Intro Prompt", "intro_prompt_entry", "intro_prompt"),
            ("H2 Prompt", "h2_prompt_entry", "h2_prompt"),
            ("H2 Brief Prompt", "h2_brief_prompt_entry", "h2_brief_prompt"),
            ("Outline Prompt", "outline_prompt_entry", "outline_prompt"),
            ("Paragraph Prompt", "paragraph_prompt_entry", "paragraph_prompt"),
            ("FAQ H2", "faq_h2_entry", "faq_h2"),
            ("FAQ Question Prompt", "faq_question_prompt_entry", "faq_question_prompt"),
            ("FAQ Answer Prompt", "faq_ans_prompt_entry", "faq_ans_prompt"),
            ("Conclusion H2", "conclusion_h2_entry", "conclusion_h2"),
            ("Conclusion Prompt", "conclusion_prompt_entry", "conclusion_prompt")
        ]

        # Condition base elements create
        self.entries = {}
        self.row = 0
        for field, var_name, db_value in self.fields:
            self.label = CTkLabel(self.scrollable_frame, text=field + ":")
            self.label.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")
            if "Outline" in field or "paragraph" in field:
                self.entry = CTkTextbox(self.scrollable_frame, height=300, width=400)
                self.entry.insert("1.0", str(getattr(self.data_check, db_value)))  # Insert the value from the database
            elif "Intro" in field or "Prompt" in field:
                self.entry = CTkTextbox(self.scrollable_frame, height=120, width=400)
                self.entry.insert("1.0", str(getattr(self.data_check, db_value)))  # Insert the value from the database
            elif "Select" in field:
                self.entry = CTkComboBox(self.scrollable_frame, state="readonly",
                                         values=['ChatGPT', 'DeepSeek', 'Gemni'], )
                self.entry.set(str(getattr(self.data_check, db_value)))
                self.entry.configure()
            else:
                self.entry = CTkEntry(self.scrollable_frame, placeholder_text=f"Enter {field.lower()}")
                self.entry.insert(0, str(getattr(self.data_check, db_value)))  # Insert the value from the database
            self.entry.grid(row=self.row, column=1, padx=10, pady=5, sticky="ew")
            self.entries[var_name] = self.entry
            self.row += 1

        # Add Save and Reset buttons
        self.save_button = CTkButton(self.scrollable_frame, width=100, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=self.row, column=0, padx=(10, 5), pady=(20, 350), sticky="ew")

        self.reset_button = CTkButton(self.scrollable_frame, width=100, text="Reset Data", command=self.reset_data)
        self.reset_button.grid(row=self.row, column=1, padx=(5, 10), pady=(20, 350), sticky="ew")

        # Configure resizing behavior -- Responsive
        def on_resize(event):
            new_width = self.winfo_width()
            for entry_name, entry_widget in self.entries.items():
                if isinstance(entry_widget, CTkEntry) or isinstance(entry_widget, CTkTextbox):
                    if new_width < 800:
                        entry_widget.configure(width=400)  # Adjust width for smaller windows
                    elif 799 < new_width < 1200:
                        entry_widget.configure(width=600)
                    else:
                        entry_widget.configure(width=1000)  # Adjust width for larger windows

        self.bind("<Configure>", on_resize)
        session.close()

    def save_changes(self):
        # Gather all values from entries
        values = {var_name: entry.get(1.0, "end-1c") if isinstance(entry, CTkTextbox) else entry.get() for
                  var_name, entry in self.entries.items()}
        session = Session()
        session.query(Postdata).filter_by(id=1).update({
            Postdata.website_name: values["website_name_entry"],
            Postdata.username: values["username_entry"],
            Postdata.app_pass: values["app_pass_entry"],
            Postdata.category_name: values["category_name_entry"],
            Postdata.chatgpt_api: values["chatgpt_api_entry"],
            Postdata.chatgpt_model: values["chatgpt_model_entry"],
            Postdata.deepseek_api: values["deepseek_api_entry"],
            Postdata.deepseek_model: values["deepseek_model_entry"],
            Postdata.gemni_api: values["gemni_api_entry"],
            Postdata.gemni_model: values["gemni_model_entry"],
            Postdata.api_select: values["api_select_entry"],
            Postdata.title_prompt: values["title_prompt_entry"],
            Postdata.intro_prompt: values["intro_prompt_entry"],
            Postdata.h2_prompt: values["h2_prompt_entry"],
            Postdata.h2_brief_prompt: values["h2_brief_prompt_entry"],
            Postdata.outline_prompt: values["outline_prompt_entry"],
            Postdata.paragraph_prompt: values["paragraph_prompt_entry"],
            Postdata.faq_h2: values["faq_h2_entry"],
            Postdata.faq_question_prompt: values["faq_question_prompt_entry"],
            Postdata.faq_ans_prompt: values["faq_ans_prompt_entry"],
            Postdata.conclusion_h2: values["conclusion_h2_entry"],
            Postdata.conclusion_prompt: values["conclusion_prompt_entry"]
        })
        session.commit()
        session.close()
        # print(f"Saved settings: {values}")

    def reset_data(self):
        """Reset data to default values."""
        try:
            # Connect to the database
            session = Session()

            # Update the database with default values
            session.query(Postdata).filter_by(id=1).update({
                Postdata.website_name: self.default_website_name,
                Postdata.username: self.default_username,
                Postdata.app_pass: self.default_app_pass,
                Postdata.category_name: self.default_category_name,
                Postdata.chatgpt_api: self.default_chatgpt_api,
                Postdata.chatgpt_model: self.default_chatgpt_model,
                Postdata.deepseek_api: self.default_deepseek_api,
                Postdata.deepseek_model: self.default_deepseek_model,
                Postdata.gemni_api: self.default_gemni_api,
                Postdata.gemni_model: self.default_gemni_model,
                Postdata.api_select: self.default_api_select,
                Postdata.title_prompt: self.default_title_prompt,
                Postdata.intro_prompt: self.default_intro_prompt,
                Postdata.h2_prompt: self.default_h2_prompt,
                Postdata.h2_brief_prompt: self.default_h2_brief_prompt,
                Postdata.outline_prompt: self.default_outline_prompt,
                Postdata.paragraph_prompt: self.default_paragraph_prompt,
                Postdata.faq_h2: self.default_faq_h2,
                Postdata.faq_question_prompt: self.default_faq_question_prompt,
                Postdata.faq_ans_prompt: self.default_faq_ans_prompt,
                Postdata.conclusion_h2: self.default_conclusion_h2,
                Postdata.conclusion_prompt: self.default_conclusion_prompt
            })

            # Commit the transaction
            session.commit()

            # Reset the UI entries to default values
            self.entries['website_name_entry'].delete(0, END)
            self.entries['website_name_entry'].insert(0, self.default_website_name)

            self.entries['username_entry'].delete(0, END)
            self.entries['username_entry'].insert(0, self.default_username)

            self.entries['app_pass_entry'].delete(0, END)
            self.entries['app_pass_entry'].insert(0, self.default_app_pass)

            self.entries['category_name_entry'].delete(0, END)
            self.entries['category_name_entry'].insert(0, self.default_category_name)

            self.entries['chatgpt_api_entry'].delete(0, END)
            self.entries['chatgpt_api_entry'].insert(0, self.default_chatgpt_api)

            self.entries['chatgpt_model_entry'].delete(0, END)
            self.entries['chatgpt_model_entry'].insert(0, self.default_chatgpt_model)

            self.entries['deepseek_api_entry'].delete(0, END)
            self.entries['deepseek_api_entry'].insert(0, self.default_deepseek_api)

            self.entries['deepseek_model_entry'].delete(0, END)
            self.entries['deepseek_model_entry'].insert(0, self.default_deepseek_model)

            self.entries['gemni_api_entry'].delete(0, END)
            self.entries['gemni_api_entry'].insert(0, self.default_gemni_api)

            self.entries['gemni_model_entry'].delete(0, END)
            self.entries['gemni_model_entry'].insert(0, self.default_gemni_model)

            self.entries['api_select_entry'].delete(0, END)
            self.entries['api_select_entry'].insert(0, self.default_api_select)

            self.entries['title_prompt_entry'].delete(0, END)
            self.entries['title_prompt_entry'].insert(0, self.default_title_prompt)

            self.entries['intro_prompt_entry'].delete(0, END)
            self.entries['intro_prompt_entry'].insert(0, self.default_intro_prompt)

            self.entries['h2_prompt_entry'].delete(0, END)
            self.entries['h2_prompt_entry'].insert(0, self.default_h2_prompt)

            self.entries['h2_brief_prompt_entry'].delete(0, END)
            self.entries['h2_brief_prompt_entry'].insert(0, self.default_h2_prompt)

            self.entries['outline_prompt_entry'].delete(0, END)
            self.entries['outline_prompt_entry'].insert(0, self.default_outline_prompt)

            self.entries['paragraph_prompt_entry'].delete(0, END)
            self.entries['paragraph_prompt_entry'].insert(0, self.default_paragraph_prompt)

            self.entries['faq_h2_entry'].delete(0, END)
            self.entries['faq_h2_entry'].insert(0, self.default_faq_question_prompt)

            self.entries['faq_question_prompt_entry'].delete(0, END)
            self.entries['faq_question_prompt_entry'].insert(0, self.default_faq_question_prompt)

            self.entries['faq_ans_prompt_entry'].delete(0, END)
            self.entries['faq_ans_prompt_entry'].insert(0, self.default_faq_ans_prompt)

            self.entries['conclusion_h2_entry'].delete(0, END)
            self.entries['conclusion_h2_entry'].insert(0, self.default_conclusion_h2)

            self.entries['conclusion_prompt_entry'].delete(0, END)
            self.entries['conclusion_prompt_entry'].insert(0, self.default_conclusion_prompt)

        except Exception as e:
            print(f"Error in reset_data: {e}")

        finally:
            # Close the database connection
            if session:
                session.close()
