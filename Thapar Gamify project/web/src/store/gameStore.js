import create from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('accessToken'),
  loading: false,
  error: null,
  
  setUser: (user) => set({ user }),
  setToken: (token) => set({ token }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    set({ user: null, token: null });
  },
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

export const useLeaderboardStore = create((set) => ({
  dailyLeaderboard: [],
  weeklyLeaderboard: [],
  allTimeLeaderboard: [],
  selectedPeriod: 'all_time',
  
  setDailyLeaderboard: (data) => set({ dailyLeaderboard: data }),
  setWeeklyLeaderboard: (data) => set({ weeklyLeaderboard: data }),
  setAllTimeLeaderboard: (data) => set({ allTimeLeaderboard: data }),
  setSelectedPeriod: (period) => set({ selectedPeriod: period }),
}));
