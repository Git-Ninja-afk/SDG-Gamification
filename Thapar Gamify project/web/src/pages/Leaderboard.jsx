import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/gameStore';
import { leaderboardService } from '../services/api';
import { motion } from 'framer-motion';

export default function Leaderboard() {
  const user = useAuthStore((state) => state.user);
  const [period, setPeriod] = useState('all_time');
  const [leaderboard, setLeaderboard] = useState([]);
  const [userRank, setUserRank] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLeaderboard();
  }, [period, user]);

  const fetchLeaderboard = async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      let response;
      if (period === 'daily') {
        response = await leaderboardService.getDailyLeaderboard(100, user.id);
      } else if (period === 'weekly') {
        response = await leaderboardService.getWeeklyLeaderboard(100, user.id);
      } else {
        response = await leaderboardService.getAllTimeLeaderboard(100, user.id);
      }
      
      setLeaderboard(response.data.leaderboard || []);
      setUserRank(response.data.user_rank);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-black py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-600 mb-2">
            🏆 Leaderboards
          </h1>
          <p className="text-gray-300">Compete with players worldwide</p>
        </motion.div>

        {/* Period Selector */}
        <div className="flex gap-4 justify-center mb-8">
          {['daily', 'weekly', 'all_time'].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                period === p
                  ? 'bg-gradient-to-r from-green-500 to-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {p === 'all_time' ? 'All Time' : p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Main Leaderboard */}
          <div className="md:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-gray-800 rounded-lg p-6 backdrop-blur-md bg-opacity-50"
            >
              <h2 className="text-2xl font-bold text-green-400 mb-4">Top Players</h2>
              
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin inline-block">⏳</div>
                </div>
              ) : (
                <div className="space-y-2">
                  {leaderboard.slice(0, 10).map((entry, idx) => (
                    <motion.div
                      key={entry.user_id}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className={`flex items-center p-4 rounded-lg ${
                        entry.user_id === user?.id
                          ? 'bg-gradient-to-r from-green-600 to-blue-600'
                          : 'bg-gray-700 hover:bg-gray-600'
                      } transition-all`}
                    >
                      <div className="text-2xl font-bold w-12 text-center">
                        {idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `#${idx + 1}`}
                      </div>
                      <div className="flex-1 ml-4">
                        <p className="font-semibold text-white">{entry.username}</p>
                        <p className="text-gray-400 text-sm">{entry.life_points} 💚</p>
                      </div>
                      <div className="text-right">
                        <p className="text-xl font-bold text-yellow-400">{entry.points}</p>
                        <p className="text-gray-400 text-sm">points</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}
            </motion.div>
          </div>

          {/* User Card */}
          {userRank && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-gradient-to-b from-green-900 to-blue-900 rounded-lg p-6 backdrop-blur-md"
            >
              <h2 className="text-xl font-bold text-green-400 mb-4">Your Rank</h2>
              <div className="text-center">
                <div className="text-6xl font-bold text-yellow-400 mb-2">
                  #{userRank.rank}
                </div>
                <p className="text-gray-300 mb-6">Out of {leaderboard.length} players</p>
                <div className="bg-gray-700 rounded-lg p-4">
                  <p className="text-gray-400 text-sm mb-2">Points</p>
                  <p className="text-3xl font-bold text-yellow-400">{userRank.points}</p>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
