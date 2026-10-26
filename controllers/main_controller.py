from flask import Blueprint, render_template, request
from models.job_scraper import JobScraper

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    """
    Ruta principal que procesa la búsqueda y renderiza los resultados.
    """
    query = request.args.get("q", "").strip()
    
    # Obtener ofertas desde el Modelo
    jobs = JobScraper.get_jobs(keyword=query) if query else JobScraper.get_jobs()
    
    # --- FILTRO DE IDIOMA / PALABRAS EN ALEMÁN ---
    palabras_prohibidas = ['Geschäftsführer', 'Teamleiter', 'm/w/d', 'Anlagenbau', 'Leiter', 'Entwicklung', 'Gesucht']
    
    jobs_filtrados = []
    for job in jobs:
        # Asegúrate de que 'title' sea la clave donde guardas el título de la oferta en tu diccionario
        titulo = job.get('title', '') 
        
        # Si el título contiene alguna palabra prohibida, nos la saltamos
        if any(palabra in titulo for palabra in palabras_prohibidas):
            continue
            
        jobs_filtrados.append(job)
    # ---------------------------------------------
    
    return render_template(
        "index.html",
        jobs=jobs_filtrados,  # <--- Pasamos la lista ya limpia
        query=query,
        total_results=len(jobs_filtrados)  # <--- Total actualizado con los filtrados
    )