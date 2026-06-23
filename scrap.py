import requests
from bs4 import BeautifulSoup
import json

# Lista de URLs
urls = [
    "http://testdeley.com/ley-39-15/titulo-1-a.php",
    "http://testdeley.com/ley-39-15/titulo-1-b.php",

    "http://testdeley.com/ley-39-15/titulo-2-a.php",
    "http://testdeley.com/ley-39-15/titulo-2-b.php",
    "http://testdeley.com/ley-39-15/titulo-2-c.php",
    "http://testdeley.com/ley-39-15/titulo-2-d.php",
    "http://testdeley.com/ley-39-15/titulo-2-e.php",
    "http://testdeley.com/ley-39-15/titulo-2-f.php",

    "http://testdeley.com/ley-39-15/titulo-3-a.php",
    "http://testdeley.com/ley-39-15/titulo-3-b.php",
    "http://testdeley.com/ley-39-15/titulo-3-c.php",

    "https://testdeley.com/ley-39-15/titulo-4-a.php",
    "https://testdeley.com/ley-39-15/titulo-4-b.php",
    "https://testdeley.com/ley-39-15/titulo-4-c.php",
    "https://testdeley.com/ley-39-15/titulo-4-d.php",
    "https://testdeley.com/ley-39-15/titulo-4-e.php",
    "https://testdeley.com/ley-39-15/titulo-4-f.php",
    "https://testdeley.com/ley-39-15/titulo-4-g.php",
    "https://testdeley.com/ley-39-15/titulo-4-h.php",
    "https://testdeley.com/ley-39-15/titulo-4-i.php",

    "http://testdeley.com/ley-39-15/titulo-5-a.php",
    "http://testdeley.com/ley-39-15/titulo-5-b.php",
    "http://testdeley.com/ley-39-15/titulo-5-c.php",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Referer": "https://google.com"
}

preguntas_json = []

# Recorremos todas las URLs
for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    listado = soup.select_one("ul#listado")
    if listado:
        for li in listado.find_all("li", recursive=False):
            texto_pregunta = li.contents[0].strip()

            opciones = []
            correcta = None

            sub_ul = li.find("ul")
            if sub_ul:
                for opcion_li in sub_ul.find_all("li", recursive=False):
                    for div in opcion_li.find_all("div"):
                        texto_opcion = div.get_text(strip=True)
                        opciones.append(texto_opcion)
                        if "correcto" in div.get("class", []):
                            correcta = texto_opcion

            preguntas_json.append({
                "pregunta": texto_pregunta,
                "opciones": opciones,
                "correcta": correcta
            })

# Guardar en JSON
with open("preguntas.json", "w", encoding="utf-8") as f:
    json.dump(preguntas_json, f, indent=4, ensure_ascii=False)

# HTML interactivo (una pregunta por vez)
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Examen Interactivo</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 30px;
      background: #f4f6f9;
      color: #333;
    }
    h1 {
      text-align: center;
      margin-bottom: 20px;
    }
    .pregunta {
      background: #fff;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      margin-bottom: 20px;
      transition: all 0.3s ease;
    }
    .opcion {
      margin: 8px 0;
    }
    .feedback {
      margin-top: 10px;
      padding: 10px;
      border-radius: 8px;
      font-weight: bold;
    }
    .correcto {
      background-color: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }
    .incorrecto {
      background-color: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }
    .botones {
      text-align: center;
      margin-top: 20px;
    }
    button {
      margin: 5px;
      padding: 10px 20px;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      font-size: 16px;
      transition: background 0.3s ease;
    }
    button:hover {
      opacity: 0.9;
    }
    .btn-primario { background: #007bff; color: white; }
    .btn-secundario { background: #6c757d; color: white; }
    .btn-correccion { background: #28a745; color: white; }
    #score {
      text-align: center;
      margin-top: 20px;
      font-size: 18px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h1>Examen Interactivo</h1>
  <div id="contenedor"></div>
  <div class="botones">
    <button class="btn-secundario" onclick="anterior()">Anterior</button>
    <button class="btn-primario" onclick="siguiente()">Siguiente</button>
    <button class="btn-correccion" onclick="corregir()">Corregir</button>
  </div>
  <p id="score"></p>

  <script>
    const preguntas = REPLACE_JSON;
    let indice = 0;
    let respuestas = {};
    let feedbacks = {};
    let corregidas = {}; // guarda si ya se corrigió esa pregunta

    // Mezclar preguntas
    preguntas.sort(() => Math.random() - 0.5);

    function mostrarPregunta() {
        const p = preguntas[indice];
        const contenedor = document.getElementById("contenedor");
        contenedor.innerHTML = "";

        let div = document.createElement("div");
        div.className = "pregunta";
        div.innerHTML = "<p><b>" + (indice+1) + ". " + p.pregunta + "</b></p>";

        p.opciones.forEach((opcion) => {
        const checked = respuestas[indice] === opcion ? "checked" : "";
        div.innerHTML += `
            <div class="opcion">
            <label>
                <input type="radio" name="preg_${indice}" value="${opcion}" ${checked}
                onchange="respuestas[indice] = this.value; corregidas[indice] = false;">
                ${opcion}
            </label>
            </div>
        `;
        });

        // Mostrar feedback previo si ya fue corregida
        if (feedbacks[indice]) {
        div.innerHTML += feedbacks[indice];
        }

        contenedor.appendChild(div);
    }

    function siguiente() {
        if (!corregidas[indice]) {
        verificarRespuesta();
        corregidas[indice] = true;
        mostrarPregunta();
        } else if (indice < preguntas.length - 1) {
        indice++;
        mostrarPregunta();
        }
    }

    function anterior() {
        if (indice > 0) {
        indice--;
        mostrarPregunta();
        }
    }

    function verificarRespuesta() {
        const p = preguntas[indice];
        const respuesta = respuestas[indice];
        if (!respuesta) return;

        if (respuesta === p.correcta) {
        feedbacks[indice] = `<div class="feedback correcto">✅ Correcto</div>`;
        } else {
        feedbacks[indice] = `<div class="feedback incorrecto">❌ Incorrecto. La respuesta correcta es: <b>${p.correcta}</b></div>`;
        }
    }

    function corregir() {
        let correctas = 0;
        let respondidas = 0;
        preguntas.forEach((p, idx) => {
        if (respuestas[idx]) {
            respondidas++;
            if (respuestas[idx] === p.correcta) {
            correctas++;
            }
        }
        });

        document.getElementById("score").innerText =
        "Has acertado " + correctas + " de " + respondidas + " preguntas respondidas.";
    }

    // Mostrar la primera pregunta
    mostrarPregunta();
    </script>

</body>
</html>
"""

html_content = html_template.replace("REPLACE_JSON", json.dumps(preguntas_json, ensure_ascii=False))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Scraping completado. Archivos 'preguntas.json' e 'index.html' generados.")
