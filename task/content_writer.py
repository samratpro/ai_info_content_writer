from task.text_generator import TextGenerator
from models import Postdata, Session
from random import choice
import re


def paragraph_format(text_for_format):
    def text_format(text):
        p_format = re.split(r'([?.!])', text.replace("<p>", "").replace("</p>", ""))
        p_format = [p_format[i] + p_format[i + 1] for i in range(0, len(p_format) - 1, 2)]
        paragraphs = [''.join(p_format[:choice([2, 3])]), ''.join(p_format[choice([2, 3]):5]),
                      ''.join(p_format[5:choice([7, 8])]), ''.join(p_format[choice([7, 8]):10]), ''.join(p_format[10:])]
        wp_paragraphs = ''.join(f'<!-- wp:paragraph --><p>{p}</p><!-- /wp:paragraph -->' for p in paragraphs if p)
        text = re.sub(r'\s{2,}', ' ', wp_paragraphs)
        text = re.sub(r'<!-- wp:paragraph --><p></p><!-- /wp:paragraph -->', '', text)
        text = re.sub(r'<p>\s+', '<p>', text)
        text = re.sub(r'\n', '', text)
        text = re.sub(r'\b\d+\.', '', text)
        return text.replace('"', '').replace("*", "")

    paragraph = ""
    splited = text_for_format.replace('<p>', '---<p>').replace('<h2>', '---<h2>').replace('<h3>', '---<h3>').replace(
        '<ul>', '---<ul>').replace('<table>', '---<table>').replace('</p>', '</p>---').replace('</h2>',
                                                                                               '</h2>---').replace(
        '</h3>', '</h3>---').replace('</ul>', '</ul>---').replace('</table>', '</table>---').strip().split(sep='---')
    for element_part in splited:
        if "<h2>" in element_part:
            formated = '<!-- wp:heading -->' + element_part + '<!-- /wp:heading -->'
        elif "<h3>" in element_part:
            formated = '<!-- wp:heading {"level":3} -->' + element_part + '<!-- /wp:heading -->'
        elif "<ul>" in element_part:
            formated = '<!-- wp:list -->' + element_part + '<!-- /wp:list -->'
        elif "<table>" in element_part:
            formated = '<!-- wp:table {"hasFixedLayout":false,"className":"is-style-stripes"} --><figure class="wp-block-table is-style-stripes">' + element_part.replace(
                "\n", "") + '</figure><!-- /wp:table -->'
        elif "<p>" in element_part:
            formated = text_format(element_part)
        else:
            formated = text_format(element_part)
        if formated != "":
            paragraph += formated
    return paragraph


class ContentWriter:
    session = Session()
    settings = session.query(Postdata).filter_by(id=1).first()
    if settings:
        api_select = settings.api_select
        if api_select == "ChatGPT":
            api_key = settings.chatgpt_api
            model = settings.chatgpt_model
        elif api_select == "DeepSeek":
            api_key = settings.deepseek_api
            model = settings.deepseek_model
        else:
            api_key = settings.gemni_api
            model = settings.gemni_model
        text_generator = TextGenerator(api_key, model, api_select)
    else:
        text_generator = TextGenerator("xxx", "xxx", "ChatGPT")

    def __init__(self, keyword, product_data, log, END):
        self.keyword = keyword
        self.product_data = product_data
        self.log = log
        self.END = END
        self.amz_tag = ContentWriter.settings.amz_tag
        self.button_text = ContentWriter.settings.button_text
        self.table_tag = ContentWriter.settings.table_tag
        self.title_prompt = ContentWriter.settings.title_prompt
        self.intro_prompt = ContentWriter.settings.intro_prompt
        self.h2_prompt = ContentWriter.settings.h2_prompt
        self.product_prompt = ContentWriter.settings.product_prompt
        self.buying_h2_prompt = ContentWriter.settings.buying_h2_prompt
        self.buying_outline_prompt = ContentWriter.settings.buying_outline_prompt
        self.buying_paragraph_prompt = ContentWriter.settings.buying_paragraph_prompt
        self.faq_h2 = ContentWriter.settings.faq_h2
        self.faq_question_prompt = ContentWriter.settings.faq_question_prompt
        self.faq_ans_prompt = ContentWriter.settings.faq_ans_prompt
        self.conclusion_h2 = ContentWriter.settings.conclusion_h2
        self.conclusion_prompt = ContentWriter.settings.conclusion_prompt

    def title_section(self):
        return ContentWriter.text_generator.text_render(self.title_prompt.replace("((keyword))", self.keyword),
                                                        self.log, self.END, "Generating Title...").replace('"', '').replace("”","")

    def intro_section(self):
        return paragraph_format(
            ContentWriter.text_generator.text_render(self.intro_prompt.replace("((keyword))", self.keyword),
                                                     self.log, self.END, "Generating Intro..."))

    def review_table_section(self):
        wp_table_h2 = '<!-- wp:heading --><h2>' + ContentWriter.text_generator.text_render(
            self.h2_prompt.replace("((keyword))", self.keyword),
            self.log, self.END, "Generating Table Heading...").replace('"', '') + '</h2><!-- /wp:heading -->'
        wp_table = '<table class="sb-pro-table"><thead><tr><th>Image</th><th>Product</th><th>Price</th></tr></thead><tbody>'
        i = 1
        for data in self.product_data:
            if i == 4:
                break
            if data["data_ok"]:
                link = data['link']
                affiliate_link = link + '?tag=' + self.amz_tag
                product_title = data['title']
                img_link = data['image']
                table_body = f'<tr><td class="sb-image"><div class="p_tag">{self.table_tag} {str(i)}</div><img src="' + img_link + '" class="p-img"></td><td class="sb-product"><div class="p_title">' + product_title + '</div></td><td class="sb-btn"><a href="' + affiliate_link + '" rel="nofollow" target="_blank">' + self.button_text + '</a></td></tr>'
                wp_table += table_body
                i += 1
        wp_table += '</tbody><style>.sb-pro-table .sb-btn a { --sev-table-color : #EF651E;background:var(--sev-table-color) !important;} </style></table>'
        return wp_table_h2 + wp_table

    def product_review_section(self):
        i = 1
        product_review_section = ''
        for data in self.product_data:
            if data["data_ok"]:
                link = data['link']
                affiliate_link = link + '?tag=' + self.amz_tag
                img_link = data['image']
                product_title = data['title']
                price = data['price']
                description = data['description']
                technical_data = data['technical_data']
                review = data['review']
                wp_h3 = '<!-- wp:heading {"level":3} --><h3>' + str(
                    i) + '. ' + product_title + '</h3><!-- /wp:heading -->'
                if len(img_link) > 0:
                    wp_img = ((
                                  '<!-- wp:image {"align":"center","sizeSlug":"large","linkDestination":"custom"} --><figure '
                                  'class="wp-block-image aligncenter size-large"><a rel="nofollow" target="_blank" href="') +
                              affiliate_link + '"><img src="' + img_link + '" alt=''/></a></figure><!-- /wp:image -->')
                else:
                    wp_img = ''
                description = paragraph_format(ContentWriter.text_generator.text_render(
                    self.product_prompt.replace("((keyword))", self.keyword).replace("((link))", link).replace(
                        "((title))",
                        product_title).replace(
                        "((description))", description).replace("((technical_data))", technical_data).replace(
                        "((review))",
                        review).replace(
                        "((price))", price),
                    self.log,
                    self.END, "Generating Product Review Section..."))
                product_review_section += wp_h3 + wp_img + description
                i += 1
        return product_review_section

    def buying_guide_section(self):
        buying_h2 = '<!-- wp:heading --><h2>' + ContentWriter.text_generator.text_render(
            self.buying_h2_prompt.replace("((keyword))", self.keyword), self.log,
            self.END, "Generating Buying h2...").replace('"', '') + '</h2><!-- /wp:heading -->'
        i = 1
        while True:
            outline_raw = ContentWriter.text_generator.text_render(
                self.buying_outline_prompt.replace('((keyword))', self.keyword), self.log,
                self.END, "Generating Buying Outline..")
            i += 1
            if any(keyword in outline_raw.lower() for keyword in ['<h2>', 'API-ERROR']):
                break
        outlines = ""
        for line in outline_raw.replace('<h2>', '---<h2>').replace('<H2>', '---<H2>').split('---'):
            if 'h2' in line.lower() and not any(
                    keyword in line.lower() for keyword in ['introduction', 'objective', 'conclusion', 'overview']):
                outlines += ' '.join(
                    l if '</' in l else l.replace('-', '').strip() + '. ' for l in line.splitlines() if len(l) > 2)
        print("Outline Generate Done...")
        outline_body_data = ''
        for heading in outlines.replace('<h2>', '---<h2>').split('---'):
            if len(heading) > 1:
                pattern = r"\b\d+\.\d+\b|[.?#@%$&()\[\]=\\/-]"
                heading_html_format = re.sub(pattern, "", heading.replace('</h2>', '<h2>---').split('---')[0])
                heading_text_format = heading_html_format.replace('<h2>', '').replace('</h2>', '').strip().capitalize()
                try:
                    topic_to_cover = heading.replace('</h2>', '<h2>---').split('---')[1].replace(' -', '').strip()
                except:
                    topic_to_cover = ''
                section = paragraph_format(ContentWriter.text_generator.text_render(
                    self.buying_paragraph_prompt.replace('((keyword))', self.keyword).replace('((heading))',
                                                                                              heading_text_format).replace(
                        '((topic_to_cover))', topic_to_cover),
                    self.log,
                    self.END, "Generating Buying Guide Paragraph Section..."))
                outline_body_data += heading + section
        print(f'Content body done...')
        return buying_h2 + outline_body_data

    def faq_section(self):
        faq_h2 = '<!-- wp:heading --><h2>' + self.faq_h2 + '</h2><!-- /wp:heading -->'
        outline = ContentWriter.text_generator.text_render(
            self.faq_question_prompt.replace('((keyword))', self.keyword), self.log, self.END,
            "Generating FAQ Questions...")
        questions = outline.splitlines()
        faq_body = ''
        schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type": "FAQPage","mainEntity":['
        for q in questions:
            q_filter = re.sub(r'[0-9]. ', '', q)
            q_h3 = '<strong>' + q_filter.title() + '</strong>'
            q_body_raw = ContentWriter.text_generator.text_render(self.faq_ans_prompt.replace('((question))', q_filter),
                                                                  self.log, self.END, "Generating FAQ Answer...")
            q_body = '<!-- wp:paragraph --><p>' + q_body_raw + '</p><!-- /wp:paragraph -->'
            faq_body += q_h3 + q_body
            question = '{"@type": "Question","name": "' + q_filter.replace('"', '').title() + '",'
            ans = '"acceptedAnswer": {"@type": "Answer","text": "' + q_body_raw.replace('"', '') + '"}},'
            schema += question + ans
        schema += ']}</script>'
        schema_final = schema.replace(',]}</script>', ']}</script>')
        faq_final = faq_h2 + faq_body + schema_final
        print('FAQ Done.................')
        return faq_final

    def conclusion_section(self):
        conclusion_h2 = '<!-- wp:heading --><h2>' + self.conclusion_h2 + '</h2><!-- /wp:heading -->'
        conclusion_para = paragraph_format(
            ContentWriter.text_generator.text_render(self.conclusion_prompt.replace('((keyword))', self.keyword),
                                                     self.log, self.END, "Generating Conclusion Section..."))
        return conclusion_h2 + conclusion_para

    def generate_content(self):
        intro = self.intro_section()
        if intro != "API-ERROR":
            return intro + self.review_table_section() + self.product_review_section() + self.buying_guide_section() + self.faq_section() + self.conclusion_section()
        else:
            return "Content Generate Error"
