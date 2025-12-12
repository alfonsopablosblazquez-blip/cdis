<template>
  <div class="tres-en-raya">
    <h2>Este es el tres en Raya</h2>
    <div class="board">
      <div 
        v-for="(cell, index) in board" 
        :key="index" 
        class="cell" 
        :class="{winner:winnerLine.includes(index)}"
        @click="makeMove(index)"
      >
        {{ cell }}
      </div>
    </div>
    <p v-if="winner"> El ganador es: {{ winner }}</p>
    <button @click="resetGame">Jugar de nuevo</button>
  </div>
</template>

<script>
export default {
  name: "TresEnRaya",
  data() {
    return {
      board: Array(9).fill(""),  
      currentPlayer: "X", 
      winner: null,  
      winnerLine: [],  
    };
  },
  methods: {
    makeMove(index)
    // si la celda está vacía y no hay ganador
    {
      if (this.board[index] === "" && !this.winner) {
        this.$set(this.board, index, this.currentPlayer);
        // vemos si con el nuevo movimiento se gana 
        if (this.checkWinner()) {
          this.winner = this.currentPlayer;
        } else 
        // cambio de turno
        {
          this.currentPlayer = this.currentPlayer === "X" ? "O" : "X";
        }
      }
    },
    checkWinner() {
      //combinaciones posibles
      const combos = [
        [0,1,2],[3,4,5],[6,7,8], 
        [0,3,6],[1,4,7],[2,5,8], 
        [0,4,8],[2,4,6]          
      ];
      for (let [a,b,c] of combos) {
        if (
        this.board[a] &&
        this.board[a] === this.board[b] &&
        this.board[a] === this.board[c]
      ) {
        this.winnerLine = [a,b,c];  // guardamos la línea ganadora
        return true;
      }
    }
    return false;
    },
    
    resetGame() {
      //volvemos a los valores inciales 
      this.board = Array(9).fill("");
      this.currentPlayer = "X";
      this.winner = null;
      this.winnerLine = []
    }
  }
};
</script>

<style scoped>
.tres-en-raya {
  text-align: center;
  margin: 20px;
}

.board {
  display: grid;
  grid-template-columns: repeat(3, 80px); /* aquí definimos las celdas 3x3 al estilo del juego*/
  grid-gap: 2px;
  justify-content: center;
  margin: 20px auto;
}

.cell {
  width: 80px;
  height: 80px;
  background: #8afff7;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2em;
  cursor: pointer;
  border: 2px solid #333;
}

.cell:hover {
  background: #58cce0;
}

.winner {
  background: rgb(38, 144, 156) !important;
  color:black;
  font-weight: bold;
}
</style>
