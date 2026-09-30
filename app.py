import streamlit as st
import json, hashlib, os, random
from datetime import datetime

st.set_page_config(page_title='AI Learning LMS', page_icon='🤖', layout='wide', initial_sidebar_state='expanded')

DATA_DIR='data'
USERS_FILE=os.path.join(DATA_DIR,'users.json')
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE,'w',encoding='utf-8') as f: json.dump({},f,indent=2)

def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def load_users():
    try:
        with open(USERS_FILE,encoding='utf-8') as f: return json.load(f)
    except: return {}
def save_users(u):
    with open(USERS_FILE,'w',encoding='utf-8') as f: json.dump(u,f,indent=2)

COURSES=[
('AI Fundamentals','Build a strong foundation in artificial intelligence, machine learning and banking use cases.','🧠',[
('What is AI?','Artificial intelligence enables software to perform tasks that normally require human-like reasoning, perception or decision making.'),('Machine Learning Basics','Machine learning finds patterns in data and uses them to make predictions or decisions.'),('AI in Banking','Banks use AI for fraud detection, credit decisions, personalization, forecasting and operations.'),('AI Project Lifecycle','A practical AI project moves from problem definition and data to modeling, evaluation, deployment and monitoring.')]),
('Generative AI','Learn how modern generative models create text, images, code and other content.','✨',[
('Generative AI Basics','Generative AI learns patterns from data and can produce new content from prompts.'),('Large Language Models','LLMs predict tokens using learned representations and attention mechanisms.'),('Prompt Engineering','Clear role, context, constraints and examples can make prompts more useful and reliable.'),('Responsible GenAI','Teams should manage hallucination, privacy, copyright, bias and human oversight.')]),
('Fraud Detection','Understand how AI identifies suspicious transactions and evolving fraud patterns.','🛡️',[
('Fraud Signals','Velocity, amount, location, device and behavioral signals can help identify unusual activity.'),('Anomaly Detection','Models can flag observations that differ strongly from expected patterns.'),('Supervised Fraud Models','Labeled historical cases can train classifiers to estimate fraud risk.'),('Fraud Model Monitoring','Monitor drift, false positives, false negatives and operational outcomes.')]),
('Credit Scoring ML','Explore machine learning workflows for credit risk and responsible scoring.','💳',[
('Credit Risk Basics','Credit scoring estimates the likelihood of repayment or default using relevant evidence.'),('Features and Labels','Features describe applicants or accounts while labels represent outcomes such as default.'),('Model Evaluation','AUC, precision, recall, calibration and stability provide different views of model performance.'),('Fairness and Explainability','Credit models require governance, explainability and checks for unfair outcomes.')]),
('AI Chatbots','Design useful AI assistants for customer service and banking workflows.','💬',[
('Chatbot Architecture','A modern assistant can combine a UI, language model, retrieval, business tools and guardrails.'),('Intent and Context','Conversation systems identify user intent and maintain useful context.'),('Retrieval-Augmented Generation','RAG retrieves trusted information before generating an answer.'),('Human Handoff','High-risk, uncertain or sensitive cases should have clear escalation paths.')]),
('Responsible AI','Learn principles for safe, fair, transparent and accountable AI.','⚖️',[
('AI Governance','Governance defines responsibilities, controls, documentation and oversight.'),('Bias and Fairness','Bias can enter through data, labels, sampling, features and deployment decisions.'),('Privacy and Security','Personal data should be protected through appropriate collection, access and retention controls.'),('Transparency','Users and reviewers need understandable information about AI use and limitations.')]),
('Risk & Compliance','Connect AI systems with model risk, regulatory controls and compliance processes.','📋',[
('Model Risk','Model risk arises when model assumptions, implementation or use lead to incorrect outcomes.'),('Controls and Documentation','Documentation should cover purpose, data, assumptions, validation, limitations and monitoring.'),('Compliance Workflows','AI controls can be integrated into approval, review, audit and incident workflows.'),('Continuous Monitoring','Post-deployment monitoring helps detect drift, failures and control breaches.')]),
('Customer Experience','Use AI to improve personalization, service quality and digital banking journeys.','🌟',[
('Personalization','AI can tailor recommendations, content and support based on customer context.'),('Next-Best Action','Models can estimate which relevant action or offer may be useful next.'),('Voice and Digital Assistants','Conversational interfaces can reduce friction while preserving secure authentication.'),('Measuring CX','Useful KPIs include resolution time, satisfaction, adoption, retention and error rates.')])]

QUIZES={
0:[('Which statement best describes AI?', ['Software that can perform tasks requiring human-like capabilities','Only a database system','A password manager','A spreadsheet'],0,'AI systems can perform tasks such as prediction, perception and language processing.'),('What is machine learning mainly used for?', ['Finding patterns in data and making predictions','Replacing all databases','Creating passwords','Formatting documents'],0,'Machine learning learns patterns from examples.'),('Which is a banking AI use case?', ['Fraud detection','Changing a monitor cable','Printing receipts manually','Formatting slides'],0,'Fraud detection is a common AI application in banking.')],
1:[('What does a generative model do?', ['Creates new content from learned patterns','Only stores files','Only sorts rows','Only checks spelling'],0,'Generative models can create new text, images, code and more.'),('What is a prompt?', ['Instructions or context given to an AI model','A database table','A network cable','A password hash'],0,'A prompt provides instructions and context for model generation.')],
2:[('Which is a fraud signal?', ['Unusual transaction velocity','Font size','Screen brightness','Keyboard layout'],0,'Transaction velocity can be a useful fraud signal.'),('What is anomaly detection?', ['Finding observations that differ from expected patterns','Encrypting a PDF','Writing CSS','Backing up photos'],0,'Anomaly detection identifies unusual observations.')],
3:[('What is a credit label?', ['An outcome used for training/evaluation','A UI color','A bank branch name','A password'],0,'A label represents the target outcome in supervised learning.'),('Which metric can help evaluate a classifier?', ['AUC','Font weight','Screen DPI','File size'],0,'AUC is a common classification evaluation metric.')],
4:[('What can RAG do?', ['Retrieve trusted information before generation','Delete all training data','Replace authentication','Compress images'],0,'Retrieval-Augmented Generation retrieves relevant information to ground answers.'),('When should a chatbot escalate?', ['When a case is high-risk or uncertain','Always after one message','Never','Only on weekends'],0,'Escalation supports safety and human oversight.')],
5:[('What is AI governance?', ['Controls, responsibilities and oversight for AI','A graphics library','A database backup','A browser extension'],0,'Governance defines how AI is controlled and overseen.'),('Bias can enter through?', ['Data and labels','Only screen size','Only CPU speed','Only file names'],0,'Bias can enter through data, labels, sampling and other stages.')],
6:[('What is model risk?', ['Risk from incorrect model assumptions, implementation or use','A UI animation','A file format','A login button'],0,'Model risk concerns incorrect outcomes caused by model-related issues.'),('Why monitor AI after deployment?', ['To detect drift and failures','To change the logo','To increase font size','To remove documentation'],0,'Continuous monitoring detects changing performance and control issues.')],
7:[('Which is a customer experience KPI?', ['Resolution time','CSS margin','CPU temperature','File extension'],0,'Resolution time is a customer service performance measure.'),('What is personalization?', ['Tailoring experiences using relevant customer context','Deleting customer records','Changing passwords','Removing analytics'],0,'Personalization adapts experiences to customer context.')]
}
# Ensure every course has a 3-question demo quiz.
for i in range(8):
    while len(QUIZES[i])<3:
        QUIZES[i].append(QUIZES[i][0])

SPONSORS=['NEXA AI','FinTech Lab','CloudNova','DataBridge','FutureSkills']

if 'page' not in st.session_state: st.session_state.page='Home'
if 'user' not in st.session_state: st.session_state.user=None
if 'progress' not in st.session_state: st.session_state.progress={}
if 'quiz_scores' not in st.session_state: st.session_state.quiz_scores={}
if 'quiz_index' not in st.session_state: st.session_state.quiz_index=0
if 'quiz_answers' not in st.session_state: st.session_state.quiz_answers={}
if 'selected_course' not in st.session_state: st.session_state.selected_course=0

# CSS
st.markdown('''<style>
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#07111f 0%,#0b1630 55%,#101a35 100%);color:#eaf2ff}
[data-testid="stHeader"]{background:rgba(0,0,0,0)}
.block-container{max-width:1200px;padding-top:1.5rem}
.hero{padding:42px;border-radius:28px;background:linear-gradient(135deg,rgba(37,99,235,.25),rgba(124,58,237,.22));border:1px solid rgba(255,255,255,.1);box-shadow:0 20px 60px rgba(0,0,0,.22)}
.hero h1{font-size:3.2rem;margin:0}.muted{color:#a9b8d0}.glass{padding:20px;border-radius:20px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.09)}
.kpi{padding:15px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);text-align:center}.kpi b{font-size:1.5rem}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:rgba(59,130,246,.16);color:#9ec5ff;font-size:.8rem}
</style>''',unsafe_allow_html=True)

def nav():
    st.sidebar.markdown('## 🤖 AI Learning')
    menu=['Home','Dashboard','Courses','Quizzes','Certificates','Profile']
    for item in menu:
        if st.sidebar.button(item,use_container_width=True,key='nav_'+item): st.session_state.page=item; st.rerun()
    st.sidebar.divider()
    if st.session_state.user:
        st.sidebar.success(f"Signed in as {st.session_state.user}")
        if st.sidebar.button('Logout',use_container_width=True): st.session_state.user=None; st.session_state.page='Home'; st.rerun()

def back():
    if st.session_state.page!='Home':
        if st.button('← Back',key='back'): st.session_state.page='Home'; st.rerun()

def home():
    st.markdown('<div class="hero"><span class="badge">AI TRAINING PLATFORM</span><h1>Learn AI. Prove Skills. Earn Certificates.</h1><p class="muted">Interactive AI-focused learning for modern banking professionals and students.</p></div>',unsafe_allow_html=True)
    st.write('')
    k1,k2,k3,k4=st.columns(4)
    for col,label,val in [(k1,'Courses','8'),(k2,'Lessons','32'),(k3,'Demo Quizzes','8'),(k4,'AI Tutor','LIVE')]:
        col.markdown(f'<div class="kpi"><span class="muted">{label}</span><br><b>{val}</b></div>',unsafe_allow_html=True)
    st.write('')
    st.subheader('Explore Learning')
    a,b,c=st.columns(3)
    if a.button('📚 Structured Courses',use_container_width=True): st.session_state.page='Courses'; st.rerun()
    if b.button('🧩 Interactive Quizzes',use_container_width=True): st.session_state.page='Quizzes'; st.rerun()
    if c.button('🏆 Earn Certificates',use_container_width=True): st.session_state.page='Certificates'; st.rerun()
    st.divider()
    st.subheader('✨ AI Generative Tutor')
    st.caption('Ask an AI learning question and receive an instant educational response. This standalone Streamlit version uses a local tutor engine and requires no API key.')
    q=st.text_input('Ask your AI Tutor',placeholder='What is generative AI?')
    if st.button('Generate Answer',type='primary') and q:
        ql=q.lower(); ans='AI is a field of computing focused on systems that perform tasks such as prediction, language understanding, perception and decision support.'
        if 'generative' in ql: ans='Generative AI creates new content such as text, images or code by learning patterns from data. In banking, it can support summarization, assistants and knowledge workflows with appropriate controls.'
        elif 'fraud' in ql: ans='AI fraud detection can combine transaction, behavioral and device signals to identify unusual activity. Models should be monitored for false positives, false negatives and drift.'
        elif 'machine learning' in ql or 'ml' in ql: ans='Machine learning learns patterns from data and uses those patterns to make predictions or decisions. Supervised learning uses labeled examples, while unsupervised learning finds structure without target labels.'
        st.info(ans)

def courses():
    back(); st.title('📚 Courses'); st.caption('Choose an AI course and complete its lessons, then take the final assessment.')
    for i,(name,desc,icon,lessons) in enumerate(COURSES):
        done=st.session_state.progress.get(str(i),0); pct=int(done/len(lessons)*100)
        with st.container(border=True):
            c1,c2,c3=st.columns([1,5,1]); c1.markdown(f'# {icon}')
            c2.markdown(f'### {name}<br><span class="muted">{desc}</span>',unsafe_allow_html=True); c2.progress(pct/100,text=f'{pct}% complete')
            if c3.button('Open',key=f'open{i}'): st.session_state.selected_course=i; st.session_state.page='Course'; st.rerun()

def course_page():
    back(); i=st.session_state.selected_course; name,desc,icon,lessons=COURSES[i]
    st.title(f'{icon} {name}'); st.write(desc)
    done=st.session_state.progress.get(str(i),0); st.progress(done/len(lessons),text=f'{done}/{len(lessons)} lessons completed')
    for j,(title,body) in enumerate(lessons):
        with st.expander(f'Lesson {j+1}: {title}',expanded=(j==done)):
            st.write(body)
            if j<=done:
                if st.button('Mark lesson complete' if j==done else 'Completed ✓',key=f'lesson{i}_{j}',disabled=j<done):
                    st.session_state.progress[str(i)]=min(j+1,len(lessons)); st.rerun()
    if done>=len(lessons):
        st.success('Course lessons complete. Your demo/final quiz is ready.')
        if st.button('🧩 Take Course Quiz',type='primary'): st.session_state.page='Quiz'; st.session_state.quiz_index=0; st.session_state.quiz_answers={}; st.rerun()

def quizzes():
    back(); st.title('🧩 Quizzes'); st.caption('Demo quizzes are available for every AI course. They are practice-only and do not affect certificates.')
    for i,(name,desc,icon,lessons) in enumerate(COURSES):
        with st.container(border=True):
            c1,c2,c3=st.columns([1,6,1]); c1.markdown(f'# {icon}'); c2.markdown(f'### {name}<br><span class="muted">3-question demo quiz</span>',unsafe_allow_html=True)
            if c3.button('Start',key=f'demo{i}'): st.session_state.selected_course=i; st.session_state.page='Quiz'; st.session_state.quiz_index=0; st.session_state.quiz_answers={}; st.rerun()

def quiz_page():
    back(); i=st.session_state.selected_course; name=COURSES[i][0]; qs=QUIZES[i]; n=st.session_state.quiz_index
    st.title(f'🧩 {name} — Demo Quiz')
    if n<len(qs):
        q,opts,correct,exp=qs[n]; st.progress(n/len(qs),text=f'Question {n+1} of {len(qs)}')
        ans=st.radio(q,opts,key=f'answer_{i}_{n}')
        if st.button('Submit Answer',type='primary'):
            idx=opts.index(ans); st.session_state.quiz_answers[n]=idx
            if idx==correct: st.success('Correct! 🎉')
            else: st.error(f'Not quite. Correct answer: {opts[correct]}')
            st.info(exp)
            if st.button('Next Question',key=f'next_{i}_{n}'): st.session_state.quiz_index+=1; st.rerun()
    else:
        score=sum(st.session_state.quiz_answers.get(x,-1)==qs[x][2] for x in range(len(qs)))
        pct=int(score/len(qs)*100); st.session_state.quiz_scores[str(i)]=pct
        st.success(f'Quiz complete — {score}/{len(qs)} ({pct}%)')
        st.write('Demo quizzes are for practice. Complete the course assessment to qualify for a certificate.')
        if st.button('Retake Quiz'): st.session_state.quiz_index=0; st.session_state.quiz_answers={}; st.rerun()
        if st.button('Back to Quizzes'): st.session_state.page='Quizzes'; st.rerun()

def dashboard():
    back(); st.title('📊 Dashboard'); completed=sum(v>=len(COURSES[int(k)][3]) for k,v in st.session_state.progress.items() if k.isdigit()); avg=int(sum(st.session_state.quiz_scores.values())/len(st.session_state.quiz_scores)) if st.session_state.quiz_scores else 0
    a,b,c=st.columns(3); a.metric('Courses Completed',completed); b.metric('Quiz Average',f'{avg}%'); c.metric('Lessons',sum(st.session_state.progress.values()))
    st.subheader('Continue Learning')
    for i,c in enumerate(COURSES):
        pct=st.session_state.progress.get(str(i),0)/len(c[3]); st.write(f'{c[2]} {c[0]}'); st.progress(pct)

def certificates():
    back(); st.title('🏆 Certificates'); st.caption('Certificates unlock when a course assessment is passed at 70% or above.')
    for i,c in enumerate(COURSES):
        score=st.session_state.quiz_scores.get(str(i),0)
        if score>=70: st.success(f'Certificate eligible: {c[0]} — score {score}%')
        else: st.info(f'{c[0]} — Complete and pass the assessment (current score: {score}%)')
    st.subheader('Certification Collaborators'); st.write(' · '.join(SPONSORS)); st.caption('Demo collaborator names — replace these with your real certification partners before production.')

def profile():
    back(); st.title('👤 Profile')
    if not st.session_state.user: st.warning('Please sign in to edit your profile.'); return
    u=load_users().get(st.session_state.user,{})
    with st.form('profile'):
        name=st.text_input('Name',u.get('name','')); branch=st.text_input('Branch / Organization',u.get('branch',''))
        if st.form_submit_button('Save Profile'):
            users=load_users(); users[st.session_state.user].update({'name':name,'branch':branch}); save_users(users); st.success('Profile saved.')

def auth():
    st.title('🤖 AI Learning LMS')
    tab1,tab2=st.tabs(['Login','Sign up'])
    with tab1:
        email=st.text_input('Email',key='login_email'); pw=st.text_input('Password',type='password',key='login_pw')
        if st.button('Login',type='primary'):
            users=load_users()
            if email in users and users[email]['password']==hash_password(pw): st.session_state.user=email; st.session_state.page='Home'; st.rerun()
            else: st.error('Invalid email or password.')
    with tab2:
        email=st.text_input('Email',key='reg_email'); name=st.text_input('Name',key='reg_name'); pw=st.text_input('Password',type='password',key='reg_pw')
        if st.button('Create Account'):
            users=load_users()
            if email in users: st.error('Account already exists.')
            elif not email or not pw: st.error('Email and password are required.')
            else: users[email]={'name':name,'password':hash_password(pw),'branch':''}; save_users(users); st.success('Account created. You can now log in.')

def main():
    nav()
    if not st.session_state.user and st.session_state.page in ['Dashboard','Profile','Certificates']: auth(); return
    p=st.session_state.page
    if p=='Home': home()
    elif p=='Courses': courses()
    elif p=='Course': course_page()
    elif p=='Quizzes': quizzes()
    elif p=='Quiz': quiz_page()
    elif p=='Dashboard': dashboard()
    elif p=='Certificates': certificates()
    elif p=='Profile': profile()
    else: home()

main()
