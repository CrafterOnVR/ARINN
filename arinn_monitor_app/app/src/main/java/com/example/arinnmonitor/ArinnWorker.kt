package com.example.arinnmonitor

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.URL

class ArinnWorker(appContext: Context, workerParams: WorkerParameters) :
    CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        try {
            val response = URL("https://arinn-monitor-default-rtdb.firebaseio.com/state.json").readText()
            val matchTopic = """"current_topic_index"\s*:\s*([\d]+)""".toRegex().find(response)
            
            if (matchTopic != null) {
                val currentTopicIndex = matchTopic.groupValues[1].toInt().coerceAtMost(4)
                
                val prefs = applicationContext.getSharedPreferences("arinn_prefs", Context.MODE_PRIVATE)
                val storedTopicIndex = prefs.getInt("last_topic_index", -1)
                
                // If the topic changed, fire a notification!
                if (storedTopicIndex != -1 && currentTopicIndex > storedTopicIndex) {
                    sendNotification(currentTopicIndex)
                }
                
                // Update local storage
                prefs.edit().putInt("last_topic_index", currentTopicIndex).apply()
            }
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }

    private fun sendNotification(topicIndex: Int) {
        val channelId = "arinn_channel"
        val notificationManager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "ARINN Phase Transitions",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Notifies when ARINN moves to the next topic."
            }
            notificationManager.createNotificationChannel(channel)
        }

        val topics = listOf(
            "Recursive Self-Improvement & Meta-Learning Algorithms",
            "Advanced Neural Network Mathematics",
            "Software Engineering & Python Architecture",
            "Formal Logic & Reasoning",
            "FINAL EXAM"
        )
        
        val newPhase = if (topicIndex < 5) topics[topicIndex] else "UNKNOWN PHASE"

        val notification = NotificationCompat.Builder(applicationContext, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("ARINN Phase Transition")
            .setContentText("Topic ${topicIndex + 1} Started: $newPhase")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        notificationManager.notify(topicIndex, notification)
    }
}
