import random
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Parchís Simplificado en Streamlit",
    page_icon="🎲",
    layout="centered",
)

# Inicializar el estado de la partida si no existe
if "pos_rojo" not in st.session_state:
  st.session_state.pos_rojo = 0  # 0 significa en casa, meta es 30
if "pos_azul" not in st.session_state:
  st.session_state.pos_azul = 0
if "turno" not in st.session_state:
  st.session_state.turno = "Rojo"  # 'Rojo' o 'Azul'
if "ultimo_dado" not in st.session_state:
  st.session_state.ultimo_dado = None
if "mensaje" not in st.session_state:
  st.session_state.mensaje = (
      "¡Bienvenidos al Parchís! Empieza el turno del jugador Rojo."
  )

META = 30  # Casilla final para ganar


def reiniciar_juego():
  st.session_state.pos_rojo = 0
  st.session_state.pos_azul = 0
  st.session_state.turno = "Rojo"
  st.session_state.ultimo_dado = None
  st.session_state.mensaje = "¡Juego reiniciado! Turno del jugador Rojo."


# Interfaz visual
st.title("🎲 Miniparchís en Streamlit")
st.markdown(
    "Un juego simplificado de 2 jugadores (Rojo vs Azul). ¡Llega a la casilla"
    f" {META} para ganar!"
)

# Mostrar estado actual del tablero
col1, col2 = st.columns(2)

with col1:
  st.markdown("### 🔴 Jugador Rojo")
  st.write(f"Posición: **{st.session_state.pos_rojo} / {META}**")
  # Barra de progreso visual
  st.progress(st.session_state.pos_rojo / META)

with col2:
  st.markdown("### 🔵 Jugador Azul")
  st.write(f"Posición: **{st.session_state.pos_azul} / {META}**")
  st.progress(st.session_state.pos_azul / META)

st.divider()

# Mensajes de estado del juego
st.info(st.session_state.mensaje)

# Control de turnos y dados
if st.session_state.pos_rojo < META and st.session_state.pos_azul < META:
  st.subheader(f"Turno actual: {st.session_state.turno}")

  if st.button("🎲 Lanzar Dado", use_container_width=True):
    dado = random.randint(1, 6)
    st.session_state.ultimo_dado = dado

    # Lógica del turno
    if st.session_state.turno == "Rojo":
      if st.session_state.pos_rojo == 0 and dado != 5 and dado != 6:
        st.session_state.mensaje = (
            f"El Rojo sacó un {dado}. Necesita un 5 o un 6 para salir de casa."
        )
      else:
        if st.session_state.pos_rojo == 0:
          st.session_state.pos_rojo = 1
          st.session_state.mensaje = (
              f"¡El Rojo sacó un {dado} y salió de casa a la casilla 1!"
          )
        else:
          st.session_state.pos_rojo += dado
          if st.session_state.pos_rojo >= META:
            st.session_state.pos_rojo = META
            st.session_state.mensaje = (
                "🎉 ¡El Jugador Rojo ha llegado a la meta y GANA el juego!"
            )
          else:
            st.session_state.mensaje = f"El Rojo avanzó {dado} casillas."

        # Cambio de turno (si no sacó 6, repite turno opcionalmente o cambia)
        if dado != 6 and st.session_state.pos_rojo < META:
          st.session_state.turno = "Azul"
        elif dado == 6:
          st.session_state.mensaje += " ¡Sacó un 6, repite turno!"

    else:  # Turno Azul
      if st.session_state.pos_azul == 0 and dado != 5 and dado != 6:
        st.session_state.mensaje = (
            f"El Azul sacó un {dado}. Necesita un 5 o un 6 para salir de casa."
        )
      else:
        if st.session_state.pos_azul == 0:
          st.session_state.pos_azul = 1
          st.session_state.mensaje = (
              f"¡El Azul sacó un {dado} y salió de casa a la casilla 1!"
          )
        else:
          st.session_state.pos_azul += dado
          if st.session_state.pos_azul >= META:
            st.session_state.pos_azul = META
            st.session_state.mensaje = (
                "🎉 ¡El Jugador Azul ha llegado a la meta y GANA el juego!"
            )
          else:
            st.session_state.mensaje = f"El Azul avanzó {dado} casillas."

        if dado != 6 and st.session_state.pos_azul < META:
          st.session_state.turno = "Rojo"
        elif dado == 6:
          st.session_state.mensaje += " ¡Sacó un 6, repite turno!"

    st.rerun()

  if st.session_state.ultimo_dado:
    st.write(f"🔢 Último resultado del dado: **{st.session_state.ultimo_dado}**")

else:
  st.success("¡Partida finalizada!")
  if st.button("🔄 Jugar de nuevo"):
    reiniciar_juego()
    st.rerun()

# Botón de reinicio general en la barra lateral
with st.sidebar:
  st.header("⚙️ Controles")
  if st.button("Reiniciar Partida"):
    reiniciar_juego()
    st.rerun()
  st.markdown("---")
  st.markdown(
      "Hecho con Python y Streamlit 🎈. Este es un modelo conceptual"
      " simplificado del clásico juego de mesa Parchís."
  )