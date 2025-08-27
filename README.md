# 🏥 Empowering Nigerian Healthcare with AI  

## 📌 Project Overview  
This project aims to **empower Nigerians with AI-driven healthcare insights** by leveraging public health facility data from [health.gov.ng](https://health.gov.ng).  
The goal is to help citizens choose the **right healthcare facility with confidence**.  

---

## 📊 Data Source  
- Data obtained from **[health.gov.ng](https://health.gov.ng)**  
- Last updated: **2023**  
- Cleaned, transformed, and structured for efficient retrieval  

---

## 🧠 Tech Stack & Architecture  
- ⚡ **RAG (Retrieval-Augmented Generation) + LLM** → intelligent, context-aware responses  
- 🚀 **Groq** → high-speed LLM inference for real-time query responses  
- 🗂 **Qdrant Vector Database** → embeddings storage + semantic search  
- 🖥 **FastAPI** → backend API layer (Qdrant + Groq LLM integration)  
- 🌐 **React.js** → frontend interface for users  
- 🐍 **Python** → programming language for data processing, AI integration, and backend logic  

---

## ⚙️ Process  
1. **Data Cleaning** → standardized and validated healthcare facility records  
2. **Vectorization & Storage** → embeddings generated & uploaded into **Qdrant**  
3. **Backend Development** → built with **FastAPI** to handle queries + connect Groq LLM  
4. **Frontend Development** → interactive interface built with **React.js**  
5. **Integration** → all components combined into a working **AI-powered healthcare recommendation tool**  

---

## 🚀 Impact  
- ✅ Provides **accessible, reliable information** on healthcare facilities in Nigeria  
- ✅ Helps patients make **informed healthcare decisions**  
- ✅ Demonstrates the **real-world power of AI (RAG + Groq + LLMs)** in public service delivery  
- ✅ Leverages **Groq’s speed** for **near real-time insights**  

---

## 🔮 Next Steps  
- 🔄 Update with **newer datasets** as they become available  
- 🏥 Expand to include **doctor specialization searches** (e.g., orthopedics, pediatrics)  
- 🌍 Add **multilingual support** (English, Pidgin, Hausa, Yoruba, Igbo)  
- ☁️ Deploy on **cloud infrastructure** for scalability  

---

## 📸 Demo / Screenshots *(Optional)*  
_Add some screenshots or GIFs of your React frontend here for visual appeal_  

---

## 💡 How to Run Locally *(Optional)*  
```bash
# Clone the repo
git clone https://github.com/yourusername/yourrepo.git  

# Navigate into the project
cd yourrepo  

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload  

# Frontend setup
cd frontend
npm install
npm start  
