import Challenge
open ThreeAgentAdditiveMaximalEf1
example : targetWitness (⟨1,[]⟩,[1]) [[],[],[]] = false := by native_decide
example : targetWitness (⟨1,[]⟩,[1]) [[0],[],[]] = true := by native_decide
example : targetWitness (⟨2,[]⟩,[1,1]) [[0,1],[],[]] = false := by native_decide
