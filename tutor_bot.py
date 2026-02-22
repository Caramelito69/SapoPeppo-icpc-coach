import discord
from discord.ext import commands
import os
import requests
from groq import Groq
from dotenv import load_dotenv

# Cargamos las variables ocultas
load_dotenv()

# Las sacamos del entorno seguro
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

historial_conversaciones = {}

usuarios_codeforces = {
    702661555216449588: "Francisco-gmail-com",
    1127084688117350451: "ellorodeantony",              
    940430103089930280: "noeliamurillouwu",
}

@bot.command(name='vincular')
async def vincular(ctx, handle: str):
    usuarios_codeforces[ctx.author.id] = handle
    await ctx.send(f"✅ Cuenta de Boscosoft vinculada a Codeforces: **{handle}**.")

@bot.event
async def on_ready():
    print("="*50)
    print(f'✅ ¡Éxito! El Entrenador SapoPeppo {bot.user} está conectado, con memoria y API de CF.')
    print("="*50)

@bot.command(name='duda')
async def duda(ctx, *, pregunta: str = None):
    if not pregunta:
        await ctx.send(f"¡Hola {ctx.author.mention}! Soy SapoPeppo. Dime, ¿en qué problema te quedaste atascado?")
        return

    usuario_id = ctx.author.id
    handle_cf = usuarios_codeforces.get(usuario_id)
    
    nivel_estudiante = "Nivel Desconocido (Asume que es un principiante entusiasta del club Boscosoft)."
    if handle_cf:
        try:
            url = f"https://codeforces.com/api/user.info?handles={handle_cf}"
            respuesta = requests.get(url).json()
            if respuesta['status'] == 'OK':
                datos_cf = respuesta['result'][0]
                rating = datos_cf.get('rating', 0)
                rank = datos_cf.get('rank', 'unrated')
                nivel_estudiante = f"Usuario de Codeforces: {handle_cf} | Rango: {rank} | Rating: {rating}."
        except Exception as e:
            print(f"No se pudo obtener el nivel de CF: {e}")

    INSTRUCCIONES_DINAMICAS = f"""
    Eres 'SapoPeppo', el entrenador de élite de programación competitiva (ICPC, IOI) del club "Boscosoft".
    
    INFORMACIÓN DEL ESTUDIANTE ACTUAL:
    {nivel_estudiante}
    
    REGLAS ESTRICTAS DE PEDAGOGÍA:
    1. GUÍA, NO RESUELVAS: NUNCA le des el problema 100% resuelto. Da pistas conceptuales, explica la lógica o señala casos base (edge cases).
    2. ADAPTA TU NIVEL: Si el rating es bajo (< 1200 o desconocido), explica paso a paso con analogías. Si es alto (> 1400), usa notación Big O y habla de optimización.
    3. VARIABLES CP: Si muestras código, usa variables de una sola letra (n, m, k, i, j) y sin espacios innecesarios.
    4. TONO: Sé motivador, empático y directo. Responde SIEMPRE EN ESPAÑOL.
    
    REGLA DE LA PLANTILLA C++:
    Si el estudiante te pide explícitamente generar un código, un esqueleto o una plantilla, DEBES usar ESTRICTAMENTE esta estructura y poner tu pista/lógica SOLAMENTE dentro de la función void solve():

    ```cpp
    #include<bits/stdc++.h>
    #define INI cin.tie(0)->sync_with_stdio(0);cout.tie(0);
    using namespace std;
    #define int ll
    #define readi(a) int a;cin>>a;
    #define readi2(a,b) int a,b;cin>>a>>b;
    #define readi3(a,b,c) int a,b,c;cin>>a>>b>>c;
    #define readi4(a,b,c,d) int a,b,c,d;cin>>a>>b>>c>>d;
    #define query readi(a) while(a--)
    #define reads(a) string a;cin>>a;
    #define fore(i,a,b) for(int i=a;i<=b;i++)
    #define forei(i,a,b) for(int i=a;i>=b;i--)
    #define all(v) begin(v),end(v)
    #define rall(v) rbegin(v),rend(v)
    #define ii pair<int,int>
    #define vi vector<int>
    #define vii vector<ii>
    #define viii vector<int,ii>
    #define vs vector<string>
    #define F first
    #define S second
    #define endl '\\n'
    typedef long long ll;
    typedef unsigned long long ull;
    typedef double long dl;
    const ll inf=numeric_limits<ll>::max();
    
    void solve()
    {{
        // SapoPeppo: Solo escribe aquí la pista o la estructura del algoritmo
    }}
    
    main()
    {{
        INI solve();
    }}
    ```
    """

    if usuario_id not in historial_conversaciones:
        historial_conversaciones[usuario_id] = [{"role": "system", "content": INSTRUCCIONES_DINAMICAS}]
    else:
        
        historial_conversaciones[usuario_id][0] = {"role": "system", "content": INSTRUCCIONES_DINAMICAS}

    historial_conversaciones[usuario_id].append({"role": "user", "content": pregunta})

    if len(historial_conversaciones[usuario_id]) > 10:
        historial_conversaciones[usuario_id] = [historial_conversaciones[usuario_id][0]] + historial_conversaciones[usuario_id][-9:]


    async with ctx.typing():
        try:
            print(f"[{ctx.author}] consultó a SapoPeppo: {pregunta}")
            
            chat_completion = client.chat.completions.create(
                messages=historial_conversaciones[usuario_id],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            
            respuesta_ia = chat_completion.choices[0].message.content
            historial_conversaciones[usuario_id].append({"role": "assistant", "content": respuesta_ia})
            
            mensaje_final = f"{ctx.author.mention}\n{respuesta_ia}"
            
            if len(mensaje_final) > 1900:
                for i in range(0, len(mensaje_final), 1900):
                    await ctx.send(mensaje_final[i:i+1900])
            else:
                await ctx.send(mensaje_final)
            
        except Exception as e:
            print(f"❌ Error con Groq: {e}")
            await ctx.send("¡Ups! SapoPeppo se quedó sin aliento. ¡Intenta de nuevo en unos segundos!")

bot.run(DISCORD_TOKEN)