import React, { useEffect, useState } from 'react';
import { recommendationService } from '../services/api';
import { useAuthStore } from '../store/gameStore';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const user = useAuthStore((state) => state.user);
  const [stats, setStats] = useState(null);
  const [recommendations, setRecommendations] = useState({ tasks: [], quizzes: [] });
  const [engagement, setEngagement] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      const [taskRecs, quizRecs, engagementData] = await Promise.all([
        recommendationService.getTaskRecommendations(user.id, 5),
        recommendationService.getQuizRecommendations(user.id, 3),
        recommendationService.getEngagement(user.id),
      ]);

      setRecommendations({
        tasks: taskRecs.data.recommendations || [],
        quizzes: quizRecs.data.recommendations || [],
      });
      setEngagement(engagementData.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-20">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-gray-400">Keep playing to make an impact on SDGs</p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Life Points', value: user?.life_points || 0, color: 'from-green-500' },
            { label: 'Total Points', value: user?.total_points || 0, color: 'from-blue-500' },
            { label: 'Level', value: user?.level || 1, color: 'from-purple-500' },
            { label: 'Engagement', value: engagement?.engagement_score || 0, color: 'from-yellow-500' },
          ].map((stat, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.1 }}
              className={`bg-gradient-to-br ${stat.color} to-gray-800 rounded-lg p-6 text-white`}
            >
              <p className="text-gray-200 text-sm mb-2">{stat.label}</p>
              <p className="text-3xl font-bold">{stat.value}</p>
            </motion.div>
          ))}
        </div>

        {/* Main Content */}
        <div className="grid md:grid-cols-3 gap-8">
          {/* Recommended Tasks */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="md:col-span-2 bg-gray-800 rounded-lg p-6"
          >
            <h2 className="text-2xl font-bold text-green-400 mb-4">Recommended Tasks</h2>
            <div className="space-y-3">
              {recommendations.tasks.map((task, idx) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className="bg-gray-700 hover:bg-gray-600 rounded-lg p-4 cursor-pointer transition-all"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-bold text-white">{task.title}</h3>
                      <p className="text-gray-400 text-sm">{task.description}</p>
                      <div className="mt-2 flex gap-2">
                        <span className="text-xs bg-blue-600 px-2 py-1 rounded text-white">
                          {task.sdg_goal}
                        </span>
                        <span className="text-xs bg-purple-600 px-2 py-1 rounded text-white">
                          {task.difficulty}
                        </span>
                      </div>
                    </div>
                    <p className="text-lg font-bold text-yellow-400">{task.points} pts</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Engagement & Quizzes */}
          <div className="space-y-6">
            {/* Engagement Card */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-gradient-to-br from-purple-900 to-gray-800 rounded-lg p-6 text-white"
            >
              <h3 className="font-bold text-lg mb-2">Engagement</h3>
              <p className="text-3xl font-bold text-yellow-400 mb-2">
                {engagement?.engagement_score || 0}%
              </p>
              <p className="text-gray-300 text-sm mb-3">{engagement?.level || 'Unknown'}</p>
              <p className="text-sm text-green-300">{engagement?.suggestion}</p>
            </motion.div>

            {/* Quizzes */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-gray-800 rounded-lg p-6"
            >
              <h3 className="font-bold text-green-400 text-lg mb-3">Featured Quizzes</h3>
              <div className="space-y-2">
                {recommendations.quizzes.map((quiz) => (
                  <div
                    key={quiz.id}
                    className="bg-gray-700 hover:bg-gray-600 p-3 rounded cursor-pointer transition-all"
                  >
                    <p className="font-semibold text-white text-sm">{quiz.title}</p>
                    <p className="text-xs text-gray-400">{quiz.sdg_goal}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
