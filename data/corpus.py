import os
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import warnings
warnings.filterwarnings("ignore")

txt_folder = "articles_txt"
os.makedirs(txt_folder, exist_ok=True)
df = pd.read_excel('media_articles.xlsx')

manual_content = {
    'Becker College': "Becker College in Massachusetts, citing a shaky financial situation made worse by the coronavirus pandemic, has announced that it is closing permanently at the end of the current academic year. The private Worcester school's trustees made the decision Sunday, the college posted on its website Monday. 'Particularly as a Becker alumna myself, this was an exceptionally painful decision for the board to come to, but one that followed many months of striving for a viable, sustainable, and responsible path to address the increasing financial pressures on our college,' trustees chair Christine Cassidy said in the statement. This year's graduation is scheduled for May, and the school will continue to provide academic support and transitional services to students through Aug. 31. Enrollment fell in 2018 and 2019, and, in response, the school took measures to ease the financial strain, including renegotiating contracts with vendors, selling some assets, consolidating departments, and reducing staff and pay, the statement said. The school had fewer than 1,700 undergraduate and graduate students enrolled, according to its fall 2020 institutional profile. The COVID-19 crisis made things worse through an 'unanticipated and significant drop in the number of students,' Becker said. 'This loss of revenue had a dramatic impact on the ability of the college to continue to maintain financial day-to-day college operations,' the statement said. Becker also looked at mergers that didn't pan out, Cassidy wrote. In conjunction with Becker's announcement, Clark University said Monday it is establishing the Becker School of Design & Technology to house Becker's renowned game design program. Many of the program's faculty and students are expected to transition to Clark, also in Worcester. Clark intends to operate the school in facilities at Becker's campus for at least a year. Becker traces its roots to 1784 when Leicester Academy was founded. Becker's Business College was founded in 1887 and the two institutions merged in 1977, according to the school's website.",
    
    'Cabrini University': "Cabrini University has announced that it will close at the end of the 2023-24 school year, with Villanova University assuming ownership of the nearby land in the Philadelphia suburbs where the fellow Roman Catholic university is located. Cabrini's interim president Helen Drinan called it 'difficult news' in a video statement Friday, saying the 66-year-old institution would graduate 'it's final class' in 2024. 'Faced with significant financial challenges, exacerbated by declining enrollment and the COVID-19 pandemic,' Drinan said, officials 'determined that there is no credible path forward that will allow Cabrini University to continue operating beyond June 2024.' Cabrini had over the years tried to boost enrollment and revenue in a number of ways such as new programs, online options and working to attract international students, and had also tried to cut expenses as much as possible, but none of that was enough to overcome the school's 'long-term structural operating deficit,' she said. Both schools emphasized that Cabrini's name will be retained, with Villanova vowing to preserve the university's legacy 'both in name and in the continuation of some of the institution's most impactful work in education, nursing, service, immigration, and the advancement of women.'",
    
    'Judson College': "The Baptist women's college had only 12 new students committed to attend in the fall. After teetering on the edge of closure for months, Judson College's Board of Trustees voted Thursday to close the Baptist women's college in July. The college, located in Marion, Ala., had been in poor financial shape for years, but its financial outlook worsened in recent months even though the college raised more than \$2.53 million this academic year. Enrollment, which had been declining for more than a decade, was dismal this spring, with only 145 students enrolled. Only 80 students were expected to return for the upcoming academic year, and only a dozen new students had committed to attend Judson in the fall. The board voted in April to approve a budget for the 2021-22 academic year, betting on new donor leads that could result in significant gifts to the college. Those gifts never materialized, according to a college press release. Two days before Thursday's board meeting, one of Judson's creditors called a note on a loan that was due and was not renewed.",
    
    'MacMurray College': "The Board of Trustees of MacMurray College announced March 27 it will close at the end of the spring semester in May 2020, ending a 174-year history in higher education. Charles O'Connell, chair of the Board of Trustees, said the Board voted unanimously to close after extensive analysis and consideration, reaching the conclusion that the school 'had no viable financial path forward,' with declining enrollments, rising competitive costs and a small endowment. He noted that alumni had been generous in a recent fundraising drive, but that it was not sufficient to reverse trends. The Board thanked MacMurray College President Dr. Beverly Rodgers for her leadership since being appointed to the job in 2019. 'Our students remain our top priority,' Dr. Rodgers said. 'Faculty and staff have gone the extra mile in transferring all our classes to online and remote learning formats — practically overnight.' She said that MacMurray has signed transfer agreements for its current students with seven area colleges. 'We will assist all students in their transfer needs, helping them ensure they are able to complete their degrees. We will also support our faculty and staff in their transitions to other positions.' The coronavirus pandemic and resulting economic disruption were recent factors that complicated MacMurray's financial condition, but they are not the principal reasons for the Board's decision to close, according to O'Connell. The college currently has 527 full-time students and 101 faculty and staff. Due to the COVID-19 pandemic, students already have moved off campus and are taking classes online. The college has not decided whether or not to hold its commencement ceremony as scheduled on May 9. Students not eligible for graduation in May will be referred to a partner institution to complete their degree. The college has negotiated transfer agreements for its students at Blackburn College, Eureka College, Greenville University, Illinois College, McKendree University, Millikin University and Monmouth College. The college was founded in 1846 by Methodist clergy as the Illinois Conference Female Academy. It is one of the oldest colleges originally for women in the United States and one of the oldest liberal arts colleges in Illinois. The name was changed in 1899 to Illinois Woman's College. In 1913, the college was granted accreditation. The name was changed again in 1930 to MacMurray College for Women. Foreseeing the coming baby boom, the college's board of trustees established MacMurray College for Men in 1955. The men's and women's colleges merged in 1969. O'Connell said the pandemic and subsequent economic disruption were factors that complicated the college's recent financial position but were not the main reasons for the closure. The status of the college's 60-acre campus, located on the east side of Jacksonville, was not immediately clear. The archive collection of the Illinois Great Rivers Conference of The United Methodist Church is located on campus at Pfeiffer Library. Conference officials will be exploring potential sites to relocate the collection in the near future.",
    
    'Marlboro College': "Marlboro College has released documents pertaining to the Board of Trustees' decision to seek a merger with Emerson College in Boston. The document release was in response to a 'challenge' issued during a community meeting Dec. 14 on the campus. In that challenge, Will Wootton, class of 1972, an administrator at Marlboro for nearly two decades between 1983 and 2002 and president of Sterling College in Craftsbury between 2006 and 2012, asked that he and others be allowed four days to review the information. '(W)ithin seven days we will deliver to the board a report showing how the college can welcome a new class in September, and begin building for the future,' said Adrian Segar, who taught at Marlboro College for 10 years, during the Dec. 14 meeting. If the group, in its own analysis, reaches the same conclusion as the board, Segar said, it will not deliver the report and will instead acknowledge, as the Board of Trustees stated, 'There is no credible evidence to suggest that Marlboro can make it on its own.' The information released on the college's website includes financial statements from 2015 through 2019 and tax returns from 2013 to 2017. Other information published on the website includes census data pertaining to U.S. birth rates, which provides information on the number of college-aged students in any given year, demonstrating sharp declines in the number of potential students in Marlboro's demographic. The website also includes a link to the Integrated Postsecondary Education Data System, a federal system that provides information including data on enrollment, admissions, human resources, finances and net tuition revenue. In addition to that information, the college has posted a link to a letter issued on Thursday by the New England Commission of Higher Education, which accredits colleges and universities in New England. The letter notes the commission's formal 'Notice of Concern' that the college is in danger of not meeting its standards. While this letter doesn't necessarily revoke Marlboro's accreditation, it serves as a reminder that that is a possibility if remedies are not taken. 'Marlboro College continues to face serious challenges with respect to finance and enrollment, as evidenced by the College's inability to substantially increase net tuition revenue and to balance its budget,' the letter reads. Over the past three years, the letter states, student revenue has decreased from \$3.6 million to \$1.7 million. And although the college has an endowment of \$35.7 million, drawing 6.5 percent from the endowment in 2019 and 18 percent in 2020 to keep the college operating is 'unsustainable.' 'The institution's (tuition) discount rate of 67 percent, while lower than the previous year's rate of 81 percent, is also unsustainable and, as candidly noted ... the high discount rate has not been effective in attracting a sufficient number of new students to the College,' states the NECHE letter. The letter noted that a merger with Emerson College is an acceptable remedy to the situation at Marlboro. 'We also concur with the College that 'a successful merger is the only way to address the financial and enrollment concerns' the Commission has identified,' the letter states. 'We are therefore, gratified to learn that Marlboro and Emerson College have formally agreed to a Term Sheet that serves as the foundation for a full merger agreement that the governing boards of both institutions are expected to approve at their respective meetings in Spring 2020.' 'The trustees believe that acting now, before the endowment is exhausted and options become extremely limited, is the most appropriate way to protect the interests of the students, faculty and Marlboro community,' stated Marlboro College Board of Trustees in a letter issued two days after the Dec. 14 meeting. In the event the proposal between the two colleges is not successful, Marlboro College has developed a plan for what is known as 'an ethical closure.' 'The institution is considering two scenarios: a two-year teach out leading to closure at the end of (fiscal year) 2021 and a three-year teach out with closure at the end of FY2022,' notes the NECHE letter. 'Marlboro has also had 'preliminary conversations' with other colleges that would be able to accommodate students unable to complete their educational programs through the proposed teach out. ... (F)ailure on the part of the College to begin teaching out its students in the event the merger with Emerson does not transpire, will lead the Commission to immediately consider stronger public action.' What that public action might be is not mentioned in the letter. In the Board of Trustees letter published following the Dec. 14 meeting, the board noted that a severance package for all staff and administrators who will lose their jobs had been approved. The details of that severance package are not publicly available.",
    
    'Pine Manor College': "At its meeting April 24, 2020, the New England Commission of Higher Education (NECHE) voted to continue the March 2020 Notation with respect to Pine Manor College. The Notation indicates the Commission's finding that the College's accreditation may be in jeopardy if current financial conditions continue or worsen with respect to the Commission's standard on Institutional Resources. In continuing the Notation, the Commission took favorable note of the College's transparency with students, prospective students, and the College community and of the institution's commitment to making a decision no later than June 30 about the coming academic year. The Commission has asked Pine Manor College to update Commission staff on any development, positive or negative, that impacts the ability of the College to meet the Commission's Standards for Accreditation. The Commission monitors institutions issued a Notation, and will require a focused evaluation within two years to assess the institution's success in addressing the identified concerns. The Commission will continue to work closely with the College as it works to stabilize its resources and looks after the well-being of its students.",
    
    'Woodbury University': "The San Diego outpost of the Woodbury School of Architecture will close permanently at the end of this semester. Why it matters: Faculty and alumni built notable projects and influenced development across urban San Diego over the school's 26-year run. Driving the news: Los Angeles-based Woodbury University this year announced a merger with the University of Redlands that includes shutting down the San Diego campus that opened in 1998. Catherine Herbst, chair of the Barrio Logan school, said the university started winding down operations three years ago, letting students and faculty transfer to the LA campus in preparation for this spring's formal end, once the last 11 students finish. By the numbers: Since its first class graduated in 2001, the school has turned out nearly 500 students from its bachelor's of architecture program. It issued 170 graduate degrees and minted 74 state-licensed architects. The intrigue: Woodbury was especially influential because of its master's in real estate development (MRED) program, which gained notoriety by creating a model that taught architects to pursue their own projects rather than work for others. Typically, developers make decisions about how a project should look and feel based on financial and zoning constraints, and then hire architects to execute those needs. Alumni and faculty from the MRED program instead are in charge of the entire project, and their architectural decision making dictates the end result. What they're saying: 'The program was a critique of the way we build buildings in the United States,' said Andrew Malick, an MRED graduate who has become a prolific developer around the region. 'Our critique was, when an architect empowered in the business of development makes decisions, better buildings and better lifestyles are the result,' he said. Between the lines: Buildings from Woodbury-affiliated architects are linked by 'an approach, not an aesthetic,' said Tyler Hanson, a graduate and professor who has built projects in Golden Hill, North Park and Azalea Park. Woodbury architect-developers pursued small or odd lots in vibrant neighborhoods, while institutional developers chased simple, big projects downtown or on the outskirts of the city. They mastered zoning laws to maximize what they could build without triggering community hearings or approvals. '(Faculty member Ted Smith) calls it civil disobedience — I just call it being smart,' Herbst said. 'Navigating zoning and procedural democracy is something we all get really good at.' The other side: The freedom Woodbury architects celebrate has also riled residents, especially over the lack of parking for many projects. The big picture: For a decade, city leaders have slashed parking mandates, increased allowed housing density and removed development restrictions — all part of Woodbury's legacy, Malick says. 'The shadow of the MRED program is a re-envisioning of how we develop infill neighborhoods,' he said. Yes, but: Those reforms — especially Complete Communities, which dramatically slashed development restrictions — eventually enticed institutional players into those neighborhoods, diminishing small developers' competitive edge. What's next: Relaxed rules on building multiunit projects on single-family lots are creating new advantages for architects and developers, Hanson said.",
    
    'B. H. Carroll Theological Seminary': "To 'eliminate redundancy in accreditation,' B.H. Carroll has withdrawn from its membership under the Commission on Accreditation of the Association for Biblical Higher Education in preparation for its merger with East Texas Baptist University. B.H. Carroll remains accredited by the Association for Theological Schools, and it will be accredited as a seminary within ETBU, pending review and approval of its merger with ETBU by the Southern Association of Colleges and Schools Commission on Colleges. 'We chose to withdraw to eliminate institutional redundancy in accreditation,' said Greg Tomlin, professor of Christian heritage and director of the Ph.D. program. 'After we achieved ATS accreditation in 2017, we no longer needed ABHE accreditation but maintained it to strengthen ties with other evangelically minded schools.' However, as an ATS-accredited seminary within a SACS-accredited university, B.H. Carroll decided 'it was time' to withdraw voluntarily from ABHE's accreditation commission. 'It saves us time, institutional resources and money,' Tomlin explained. In a Jan. 3 letter to ABHE, B.H. Carroll President Gene Wilkes said the association has been 'a valued partner in our shared mission of biblical theological education since 2012.' ABHE was the first group to accredit B.H. Carroll after examining the quality of its programs and faculty, as well as the unique nature of its model, using online instruction to provide theological education to students where they live and work. B.H. Carroll will always be grateful and remain committed to helping ABHE maintain its role in supporting biblical higher education, Wilkes said. 'God is doing great things through ABHE, and you have my personal support and prayers as we move into God's future for us all,' Wilkes wrote to the group's commissioners. ETBU administrators plan to explore affiliate membership with the association after the merger is complete to maintain the seminary's ties with ABHE. 'Our notification was a procedural requirement to comply with ABHE standards for accredited member institutions, but withdrawal was not required because of the merger,' Tomlin said. Withdrawal from ABHE's accreditation commission has no effect on students who have received a degree from B.H. Carroll, he noted. 'Their past degrees were and remain accredited,' he said. B.H. Carroll will continue to offer certificate programs for students who want graduate-level instruction but who are not seeking a degree, he added."
}

def extract_article_metadata_and_text(url):
    """Extracts metadata prioritizing Open Graph tags to ensure accuracy, using cloudscraper for 403 bypass."""
    title, author, text = "Unknown", "Unknown", "No content extracted"
    
    if pd.isna(url) or not isinstance(url, str):
        return title, author, "Unknown", text
        
    source = urlparse(url).netloc.replace('www.', '')
    
    try:
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
        
        response = scraper.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            title = og_title['content']
        else:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
            elif soup.find('title'):
                title = soup.find('title').get_text(strip=True).split('|')[0].replace('Higher Ed Dive', '').strip('- ')

        meta_author = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', property='article:author')
        if meta_author and meta_author.get('content'):
            author = meta_author['content'].split('/')[-1].replace('-', ' ').title()
        elif soup.find(attrs={"rel": "author"}):
            author = soup.find(attrs={"rel": "author"}).get_text(strip=True)
        else:
            author_tag = soup.find(class_=lambda x: x and ('author' in x.lower() or 'byline' in x.lower()))
            if author_tag:
                author_text = author_tag.get_text(strip=True)
                author = author_text.replace('By', '').replace('by', '').replace('Published', '').strip()
                if len(author) > 50: 
                    author = "Unknown"

        for tag in soup.find_all(['header', 'footer', 'aside', 'nav', 'script', 'style']):
            tag.decompose()
            
        article_container = soup.find('div', class_='large medium article-body')
        if not article_container:
            possible_selectors = [
                ('article', None),
                ('div', ['article', 'content', 'post', 'article-body', 'story', 'main-content']),
                ('section', ['article', 'content', 'post'])
            ]
            for tag_name, class_names in possible_selectors:
                if class_names:
                    for c_name in class_names:
                        container = soup.find(tag_name, class_=lambda x: x and c_name in x.lower())
                        if container:
                            article_container = container
                            break
                else:
                    container = soup.find(tag_name)
                    if container:
                        article_container = container
                        break
                if article_container: break

        if article_container:
            paragraphs = article_container.find_all('p')
            extracted_text = ' '.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if extracted_text:
                text = extracted_text

    except Exception as e:
        print(f"  [!] Failed to scrape {url}: {e}")
        
    return title, author, source, text


metadata_records = []

for index, row in df.iterrows():
    college_name = row['name']
    url = row.get('links', '')
    
    raw_uid = row.get('UID')
    if pd.isna(raw_uid):
        uid_str = college_name.replace(' ', '_').replace('.', '').replace(',', '').lower()
    else:
        uid_str = str(int(raw_uid))
        
    print(f"Processing: {college_name} ({uid_str})...")
    
    title, author, source, text = extract_article_metadata_and_text(url)
    
    if college_name in manual_content:
        text = manual_content[college_name]
        
    relative_link = f"{txt_folder}/{uid_str}.txt"
    with open(relative_link, "w", encoding="utf-8") as f:
        f.write(text)
        
    metadata_records.append({
        'uid': uid_str,
        'college name': college_name,
        'article author': author,
        'article title': title,
        'article source': source,
        'relative link to txt file': relative_link
    })
    
    time.sleep(2)

final_df = pd.DataFrame(metadata_records)
final_df.to_excel("article_corpus_metadata.xlsx", index=False)
# final_df.to_csv("article_corpus_metadata.csv", index=False)