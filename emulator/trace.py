import numpy as np

from .state import State, initialize_state_from_rom
from .state import Uint16Registers as U16
from .state import Uint8Registers as U8
from .state import FlagsRegisters as F

from .step import step


class StateDiff():
	def __init__(self, state: State, state_prime: State):
		D_REG_UINT8 = state.REG_UINT8 - state_prime.REG_UINT8
		self.delta_REG_UINT8_IDS = np.where(D_REG_UINT8 != 0)[0]
		self.delta_REG_UINT8_VALUES = D_REG_UINT8[self.delta_REG_UINT8_IDS]
		
		D_REG_UINT16 = state.REG_UINT16 - state_prime.REG_UINT16
		self.delta_REG_UINT16_IDS = np.where(D_REG_UINT16 != 0)[0]
		self.delta_REG_UINT16_VALUES = D_REG_UINT16[self.delta_REG_UINT16_IDS]

		D_FLAGS = state.FLAGS ^ state_prime.FLAGS
		self.delta_FLAGS_IDS = np.where(D_FLAGS != 0)[0]
		self.delta_FLAGS_VALUES = D_FLAGS[self.delta_FLAGS_IDS]

		D_MEM = state.MEM - state_prime.MEM
		self.delta_MEM_ADDRS = np.where(D_MEM != 0)[0]
		self.delta_MEM_DATA = D_MEM[self.delta_MEM_ADDRS]

	def apply(self, state: State):
		state.REG_UINT8[self.delta_REG_UINT8_IDS] += self.delta_REG_UINT8_VALUES
		state.REG_UINT16[self.delta_REG_UINT16_IDS] += self.delta_REG_UINT16_VALUES
		state.FLAGS[self.delta_FLAGS_IDS] ^= self.delta_FLAGS_VALUES
		state.MEM[self.delta_MEM_ADDRS] += self.delta_MEM_DATA

		return state


	def __repr__(self):
		rep = '--- 8-bit Registers --- \n'

		for i in range(self.delta_REG_UINT8_IDS.shape[0]):
			rep += f'Δ{U8.to_string(self.delta_REG_UINT8_IDS[i])}: {hex(self.delta_REG_UINT8_VALUES[i])}\n'

		rep += '--- 16-bit Registers --- \n'

		for i in range(self.delta_REG_UINT16_IDS.shape[0]):
			rep += f'Δ{U16.to_string(self.delta_REG_UINT16_IDS[i])}: {hex(self.delta_REG_UINT16_VALUES[i])}\n'

		rep += '--- Memory --- \n'

		for i in range(self.delta_MEM_ADDRS.shape[0]):
			rep += f'Δ{hex(self.delta_MEM_ADDRS[i])}: {hex(self.delta_MEM_DATA[i])}\n'

		return rep


class Trace():
	# do this in a way tha minimizes GC
	# on the state objects. Ideally two state 
	# objects that are never deleted, just ping-ponged between?
	def __init__(self, initial_state: State):
		self.current_state_pointer = 0
		next_state = initial_state.clone()
		step(next_state)

		self.states = [initial_state, next_state]
		self.diffs = [StateDiff(self.states[0], self.states[1])]

	def step_forward(self):
		self.current_state_pointer = (self.current_state_pointer + 1) % 2 # = len(self.states)
		next_state_pointer = (self.current_state_pointer + 1) % 2 # = len(self.states)

		# this double stepping approach allows us to ping-pong 
		# back and forth between two state objects without ever
		# having to do new allocations. All the allocations are 
		# in the StateDiffs, but the state objects themselves
		# (which are much larger), are never reallocated beyond init.
		
		# we step twice because the other saved state already has 
		# already stepped to the next state.
		step( self.states[next_state_pointer] ) 
		step( self.states[next_state_pointer] )

		# then we get the diff between the current state and the next state
		self.diffs.append(StateDiff(self.states[self.current_state_pointer], self.states[next_state_pointer]))

		# and we're done.

	def step_backward(self):
		if len(self.diffs) < 2: return # can't step back if you haven't stepped yet.

		prev_state_pointer = (self.current_state_pointer + 1) % 2 # = len(self.states)
		
		diff_one = self.diffs.pop()
		diff_two = self.diffs[-1] # the second diff is relevant still for the next backward op.

		diff_one.apply(self.states[prev_state_pointer])
		diff_two.apply(self.states[prev_state_pointer])

		self.current_state_pointer = prev_state_pointer


	def current_state(self):
		return self.states[self.current_state_pointer]



