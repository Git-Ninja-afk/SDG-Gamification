import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Image,
  Dimensions,
} from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import LinearGradient from 'react-native-linear-gradient';
import { useAuthStore, useGameStore } from '../store/gameStore';

const screenWidth = Dimensions.get('window').width;

export default function DashboardScreen({ navigation }) {
  const user = useAuthStore((state) => state.user);
  const gameState = useGameStore();
  const [loading, setLoading] = useState(false);

  const chartData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [120, 150, 180, 200, 170, 210, 240],
        color: () => '#00FF00',
      },
    ],
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <LinearGradient
        colors={['#1a1a2e', '#16213e']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <Text style={styles.greeting}>Welcome back! 👋</Text>
          <Text style={styles.username}>{user?.username}</Text>
        </View>
      </LinearGradient>

      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        {[
          { label: 'Life Points', value: gameState.lifePoints, icon: '💚' },
          { label: 'Total Points', value: gameState.totalPoints, icon: '⭐' },
          { label: 'Level', value: gameState.level, icon: '🏆' },
          { label: 'Rank', value: gameState.currentRank?.rank || '-', icon: '🥇' },
        ].map((stat, idx) => (
          <LinearGradient
            key={idx}
            colors={['#00FF00', '#00AA00']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.statCard}
          >
            <Text style={styles.statIcon}>{stat.icon}</Text>
            <Text style={styles.statLabel}>{stat.label}</Text>
            <Text style={styles.statValue}>{stat.value}</Text>
          </LinearGradient>
        ))}
      </View>

      {/* Progress Chart */}
      <View style={styles.chartContainer}>
        <Text style={styles.sectionTitle}>Weekly Progress</Text>
        <LineChart
          data={chartData}
          width={screenWidth - 40}
          height={220}
          chartConfig={{
            backgroundColor: '#1a1a2e',
            backgroundGradientFrom: '#1a1a2e',
            backgroundGradientTo: '#16213e',
            color: (opacity = 1) => `rgba(0, 255, 0, ${opacity})`,
            style: {
              borderRadius: 16,
            },
          }}
          style={styles.chart}
        />
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtonsContainer}>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Tasks')}
        >
          <Text style={styles.actionButtonText}>📋 Browse Tasks</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Quizzes')}
        >
          <Text style={styles.actionButtonText}>🧠 Take Quiz</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Games')}
        >
          <Text style={styles.actionButtonText}>🎮 Play Games</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Leaderboard')}
        >
          <Text style={styles.actionButtonText}>🏅 Leaderboards</Text>
        </TouchableOpacity>
      </View>

      {/* Recent Achievements */}
      {gameState.achievements.length > 0 && (
        <View style={styles.achievementsContainer}>
          <Text style={styles.sectionTitle}>Recent Achievements</Text>
          {gameState.achievements.slice(-3).map((achievement, idx) => (
            <View key={idx} style={styles.achievementItem}>
              <Text style={styles.achievementIcon}>🏅</Text>
              <View style={styles.achievementContent}>
                <Text style={styles.achievementTitle}>{achievement.title}</Text>
                <Text style={styles.achievementDesc}>{achievement.description}</Text>
              </View>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f0f1e',
  },
  header: {
    padding: 20,
    paddingTop: 40,
  },
  headerContent: {
    marginBottom: 10,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  username: {
    fontSize: 16,
    color: '#00FF00',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 10,
    justifyContent: 'space-between',
  },
  statCard: {
    width: '48%',
    marginBottom: 15,
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
  },
  statIcon: {
    fontSize: 28,
    marginBottom: 8,
  },
  statLabel: {
    color: 'white',
    fontSize: 12,
    marginBottom: 5,
  },
  statValue: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
  },
  chartContainer: {
    backgroundColor: '#1a1a2e',
    marginHorizontal: 20,
    marginVertical: 20,
    padding: 15,
    borderRadius: 12,
  },
  sectionTitle: {
    color: '#00FF00',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  actionButtonsContainer: {
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  actionButton: {
    backgroundColor: '#00AA00',
    paddingVertical: 15,
    borderRadius: 12,
    marginBottom: 10,
    alignItems: 'center',
  },
  actionButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  achievementsContainer: {
    backgroundColor: '#1a1a2e',
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 15,
    borderRadius: 12,
  },
  achievementItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  achievementIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  achievementContent: {
    flex: 1,
  },
  achievementTitle: {
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 3,
  },
  achievementDesc: {
    color: '#888',
    fontSize: 12,
  },
});
