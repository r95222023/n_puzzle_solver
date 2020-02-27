'use strict';

function getGoalState(n){
    let goalState = [];
    for(let i=0; i<(n-1); i++){
        goalState.push(i+1);
    }
    goalState.push(0);
    return goalState;
}

function move(state, pos, relPos) {
    let newState;
    newState = state.slice(); //copy state
    swap(newState, pos, pos + relPos);
    return newState;
}

function swap(state, from, to) {
    let cache = state[from];
    state[from] = state[to];
    state[to] = cache;
}

function compare(arr1, arr2) {
    if (!arr1 || !arr2) {
        return false;
    }

    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) {
            return false;
        }
    }
    return true;
}

function getStateId(state){
    return state.join('-');
}

/* This post on stackexchange explained the condition when a puzzle
   is unsolvable http://math.stackexchange.com/a/838818
*/
function checkSolvable(state, sideSize) {
    const pos = state.indexOf(0);
    let _state = state.slice();
    _state.splice(pos,1);
    let count = 0;
    for (let i = 0; i < _state.length; i++) {
        for (let j = i + 1; j < _state.length; j++) {
            if (_state[i] > _state[j]) {
                count++;
            }
        }
    }
    return count % (sideSize-1) === 0;
}

class Bfs {
    constructor(init) {
        //EX: init = {213456780: null} for initial state [2,1,3,4,5,6,7,8,0]
        let n =0;
        this.isSolvable =true;
        let initStates = [];
        for (let key in init){
            //init has only one object inside, use loop to get the initial state
            const initState = key.split('-');
            //rebuild initial state by using string.split method
            initState.forEach((num, index)=>{
                initState[index] = Number(num)
                //make array contain only numbers
            });
            initStates.push(initState);
            n = initState.length;
            this.isSolvable = checkSolvable(initState, Math.sqrt(n));
        }


        const that = this;
        const sideSize = Math.sqrt(n);
        const moves = [
            {
                to: 'up', relPos: -1*sideSize, isMovable: (row, col) => {
                    return (row > 0)
                }
            },
            {
                to: 'left', relPos: -1, isMovable: (row, col) => {
                    return (col > 0)
                }
            },
            {
                to: 'down', relPos: sideSize, isMovable: (row, col) => {
                    return (row < (sideSize - 1))
                }
            },
            {
                to: 'right', relPos: 1, isMovable: (row, col) => {
                    return (col < (sideSize - 1))
                }
            }
        ];
        this.states = init || {};
        this.cost = 0;
        this.goalState = getGoalState(n);
        this.move = move;
        this.getChildren = (state) => {
            let newState;
            let children = [];
            let pos = state.indexOf(0);
            let row = Math.floor(pos / sideSize);
            let col = pos % sideSize;
            let stateId = getStateId(state);
            moves.forEach((direction) => {
                if (direction.isMovable(row, col)) {
                    newState = move(state, pos, direction.relPos);
                    const newStateId = getStateId(newState);
                    if (typeof that.states[newStateId] === 'undefined') {
                        that.states[newStateId] = stateId; //trace back to last state for later use
                        children.push(newState);
                    }
                }
            });
            return children;
        };
        this.traceBack = (state) => {
            const stateId = getStateId(state);
            let steps = [stateId];
            let previous = that.states[stateId];
            while (previous) {
                steps.push(previous);
                previous = that.states[previous];
            }
            return steps;
        };
        this.breadthSearch = (states) => {
            let steps, children = [];
            states.forEach((state) => {
                this.cost++;
                if (compare(that.goalState, state)) {
                    console.log('Bingo!!');
                    steps= {steps: that.traceBack(state).reverse()};
                } else {
                    that.getChildren(state).forEach((childState) => {
                        children.push(childState);
                    })
                }
            });
            return steps || children
        };
        this.engage = (states) => {
            const startTime = new Date();
            let search = that.breadthSearch(initStates || states);
            let i= 0;
            console.log(`start with: ${initStates}`);
            if(that.isSolvable){
                while (search.length) {
                    i++;
                    search = that.breadthSearch(search);
                    // console.log(`depth: ${i}`)
                }
                const endTime = new Date();
                console.log(`Total time: ${endTime-startTime}ms`);
                console.log(`Cost: ${that.cost} steps.`);
                console.log(`Depth: ${search.steps.length}`);
                console.log(`Solution: ${JSON.stringify(search.steps)}`);
            } else {
                console.log(`Warning: the initial state is not solvable!`)
            }
            return search;
        }
    }
}


module.exports = Bfs;