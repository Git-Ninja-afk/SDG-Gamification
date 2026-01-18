import create from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  loading: false,
  
  setUser: (user) => set({ user }),
  setToken: (token) => set({ token }),
  logout: () => set({ user: null, token: null }),
}));

export const useGameStore = create((set) => ({
  lifePoints: 0,
  totalPoints: 0,
  level: 1,
  achievements: [],
  currentRank: null,
  
  updatePoints: (life, total) => set({ lifePoints: life, totalPoints: total }),
  addAchievement: (achievement) => set((state) => ({
    achievements: [...state.achievements, achievement]
  })),
  setRank: (rank) => set({ currentRank: rank }),
}));
