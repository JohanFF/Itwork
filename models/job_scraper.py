import requests

class JobScraper:
    """
    Modelo unificado para extraer, filtrar por idioma (Inglés/Español)
    y combinar ofertas de empleo remoto desde 4 fuentes públicas distintas.
    """
    
    @classmethod
    def get_jobs(cls, keyword=None):
        all_jobs = []
        
        # Consultar las 4 fuentes
        all_jobs.extend(cls._fetch_remoteok())
        all_jobs.extend(cls._fetch_arbeitnow())
        all_jobs.extend(cls._fetch_jobicy())
        all_jobs.extend(cls._fetch_himalayas())
        
        # Filtrar idiomas no deseados (como alemán)
        cleaned_language_jobs = [job for job in all_jobs if not cls._is_foreign_language(job["title"])]
        
        # Filtrar por término de búsqueda si el usuario ingresó algo en la barra
        if keyword:
            term = keyword.lower().strip()
            filtered_jobs = []
            for job in cleaned_language_jobs:
                title = job["title"].lower()
                company = job["company"].lower()
                tags = [t.lower() for t in job["tags"]]
                
                if term in title or term in company or any(term in tag for tag in tags):
                    filtered_jobs.append(job)
            return filtered_jobs

        return cleaned_language_jobs

    @staticmethod
    def _is_foreign_language(text):
        foreign_words = ["entwickler", "ingenieur", "gesucht", "praktikum", "mit", "für", "und", "vollzeit"]
        text_lower = text.lower()
        return any(word in text_lower for word in foreign_words)

    @staticmethod
    def _fetch_remoteok():
        url = "https://remoteok.com/api"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()[1:]
                return [{
                    "title": item.get("position", "Sin título"),
                    "company": item.get("company", "Empresa confidencial"),
                    "location": item.get("location", "Remoto"),
                    "url": item.get("url", "#"),
                    "tags": item.get("tags", [])[:3],
                    "date": item.get("date", "")[:10],
                    "source": "RemoteOK"
                } for item in data[:10]]
        except Exception:
            pass
        return []

    @staticmethod
    def _fetch_arbeitnow():
        url = "https://www.arbeitnow.com/api/job-board-api"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json().get("data", [])
                return [{
                    "title": item.get("title", "Sin título"),
                    "company": item.get("company_name", "Empresa confidencial"),
                    "location": "Remoto" if item.get("remote") else "Global",
                    "url": item.get("url", "#"),
                    "tags": item.get("tags", [])[:3],
                    "date": "",
                    "source": "Arbeitnow"
                } for item in data[:10]]
        except Exception:
            pass
        return []

    @staticmethod
    def _fetch_jobicy():
        url = "https://jobicy.com/api/v2/remote-jobs?count=10&industry=dev"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json().get("jobs", [])
                return [{
                    "title": item.get("jobTitle", "Sin título"),
                    "company": item.get("companyName", "Empresa confidencial"),
                    "location": item.get("jobGeo", "Remoto Global"),
                    "url": item.get("url", "#"),
                    "tags": [item.get("jobCategory", "Dev")] if item.get("jobCategory") else ["Tech"],
                    "date": item.get("pubDate", "")[:10],
                    "source": "Jobicy"
                } for item in data]
        except Exception:
            pass
        return []

    @staticmethod
    def _fetch_himalayas():
        url = "https://himalayas.app/jobs/api?limit=10"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json().get("jobs", [])
                return [{
                    "title": item.get("title", "Sin título"),
                    "company": item.get("companyName", "Empresa confidencial"),
                    "location": "Remoto",
                    "url": item.get("applicationUrl", item.get("url", "#")),
                    "tags": item.get("categories", [])[:3],
                    "date": "",
                    "source": "Himalayas"
                } for item in data]
        except Exception:
            pass
        return []