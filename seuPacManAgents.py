from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Agente Minimax para o Pac-Man.
    """

    def getAction(self, gameState):
        """
        Retorna a melhor ação para o Pac-Man usando Minimax.
        """

        def minimax(agentIndex, depth, state):
            # Condição de parada: jogo acabou ou profundidade máxima atingida
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # Próximo agente
            nextAgent = (agentIndex + 1) % state.getNumAgents()
            nextDepth = depth + 1 if nextAgent == 0 else depth

            # Turno do Pac-Man (Max)
            if agentIndex == 0:
                maxScore = -float('inf')
                bestAction = None
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, successor)
                    if score > maxScore:
                        maxScore = score
                        bestAction = action
                # Na primeira chamada (getAction), retornamos a ação
                if depth == 0:
                    return bestAction
                else:
                    return maxScore

            # Turno dos Fantasmas (Min)
            else:
                minScore = float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, successor)
                    if score < minScore:
                        minScore = score
                return minScore

        # Chamada inicial do Minimax dentro do getAction
        return minimax(0, 0, gameState)




def betterEvaluationFunction(currentGameState: GameState):
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    # Calcula a distância de Manhattan para a comida mais próxima
    foodDistances = [manhattanDistance(pos, f) for f in food]
    if len(foodDistances) > 0:
        minFoodDistance = min(foodDistances)
    else:
        minFoodDistance = 0

    # Distância para o fantasma mais próximo
    ghostDistances = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    minGhostDistance = min(ghostDistances)

    # Aumenta a pontuação se o fantasma estiver assustado, mas penaliza se estiver muito perto
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignora fantasmas assustados

    return currentGameState.getScore() - (1.5 / (minFoodDistance + 1)) + (2 / (minGhostDistance + 1))

# Abbreviation
better = betterEvaluationFunction
