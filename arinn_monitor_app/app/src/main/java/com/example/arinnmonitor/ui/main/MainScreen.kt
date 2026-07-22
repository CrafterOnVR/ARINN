package com.example.arinnmonitor.ui.main

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import java.time.Instant
import java.time.Duration

import java.net.URL
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

@Composable
fun MainScreen(modifier: Modifier = Modifier) {
    var serverElapsedSeconds by remember { mutableStateOf(0L) }
    var localElapsedSeconds by remember { mutableStateOf(0L) }
    var serverTopicIndex by remember { mutableStateOf(0) }
    var lastSyncInstant by remember { mutableStateOf(Instant.now()) }
    var connectionStatus by remember { mutableStateOf("Connecting to Firebase...") }
    var activeNodes by remember { mutableStateOf("Awaiting Payload...") }
    var apiLatency by remember { mutableStateOf("Awaiting Payload...") }

    // Cloud Polling Tunnel (Every 20s to guarantee new payloads)
    LaunchedEffect(Unit) {
        while (true) {
            try {
                val response = withContext(Dispatchers.IO) {
                    URL("https://arinn-monitor-default-rtdb.firebaseio.com/state.json").readText()
                }
                val matchSeconds = """"active_elapsed_seconds"\s*:\s*([\d.]+)""".toRegex().find(response)
                val matchTopic = """"current_topic_index"\s*:\s*([\d]+)""".toRegex().find(response)
                val matchNodes = """"active_nodes"\s*:\s*([\d]+)""".toRegex().find(response)
                val matchLatency = """"api_latency_ms"\s*:\s*([\d.]+)""".toRegex().find(response)
                
                if (matchNodes != null) activeNodes = matchNodes.groupValues[1]
                if (matchLatency != null) apiLatency = matchLatency.groupValues[1] + " ms"
                
                if (matchSeconds != null) {
                    val newPayloadSeconds = matchSeconds.groupValues[1].toDouble().toLong()
                    if (matchTopic != null) {
                        serverTopicIndex = matchTopic.groupValues[1].toInt()
                    }
                    
                    if (newPayloadSeconds == serverElapsedSeconds && serverElapsedSeconds > 0L) {
                        connectionStatus = "DISCONNECTED - PC OFFLINE"
                    } else {
                        serverElapsedSeconds = newPayloadSeconds
                        lastSyncInstant = Instant.now()
                        connectionStatus = "LIVE: Syncing with PC"
                    }
                } else {
                    connectionStatus = "Awaiting first PC broadcast..."
                }
            } catch (e: Exception) {
                connectionStatus = "DISCONNECTED - CLOUD OFFLINE"
            }
            delay(20000)
        }
    }

    // Client-Side Prediction (Smooth Mathematical Interpolation)
    LaunchedEffect(serverElapsedSeconds, lastSyncInstant, connectionStatus) {
        while (true) {
            if (connectionStatus.startsWith("LIVE")) {
                val drift = Duration.between(lastSyncInstant, Instant.now()).seconds
                localElapsedSeconds = serverElapsedSeconds + drift
            } else {
                localElapsedSeconds = serverElapsedSeconds
            }
            delay(100) // Update UI at high refresh rate
        }
    }
    
    val elapsedSeconds = localElapsedSeconds
    val currentTopicIndex = serverTopicIndex.coerceAtMost(4)
    
    val topics = listOf(
        "Recursive Self-Improvement & Meta-Learning Algorithms",
        "Advanced Neural Network Mathematics",
        "Software Engineering & Python Architecture",
        "Formal Logic & Reasoning"
    )
    
    val currentTopic = if (currentTopicIndex < 4) topics[currentTopicIndex] else "FINAL EXAM"
    val isFinalExam = elapsedSeconds >= (288L * 3600L)
    
    val nextCheckpointSec = if (isFinalExam) {
        (336L * 3600L) - elapsedSeconds
    } else {
        ((currentTopicIndex + 1) * (72L * 3600L)) - elapsedSeconds
    }
    
    val remainingHours = nextCheckpointSec / 3600
    val remainingMins = (nextCheckpointSec % 3600) / 60
    val remainingSecs = nextCheckpointSec % 60

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "ARINN GENESIS",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(text = connectionStatus, fontSize = 16.sp, color = if (connectionStatus.startsWith("LIVE")) Color(0xFF00AA00) else Color.Red)
        
        Spacer(modifier = Modifier.height(48.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth().padding(8.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("CURRENT PHASE", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary)
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = if (isFinalExam) "48-HOUR FINAL EXAM" else "TOPIC ${currentTopicIndex + 1}/4",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Medium
                )
                Text(text = currentTopic, fontSize = 16.sp, color = Color.DarkGray)
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text("NEXT CHECKPOINT IN:", fontWeight = FontWeight.Bold)
        Text(
            text = String.format("%02d:%02d:%02d", remainingHours.coerceAtLeast(0), remainingMins.coerceAtLeast(0), remainingSecs.coerceAtLeast(0)),
            fontSize = 48.sp,
            fontWeight = FontWeight.ExtraBold,
            color = if (remainingHours < 1) Color.Red else Color.Black
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        LinearProgressIndicator(
            progress = { (elapsedSeconds.toFloat() / (336f * 3600f)).coerceIn(0f, 1f) },
            modifier = Modifier.fillMaxWidth().height(12.dp)
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text("Total Genesis Progress: ${(elapsedSeconds / 3600)} / 336 Hours")
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Live Telemetry Diagnostic Panel
        Card(
            modifier = Modifier.fillMaxWidth().padding(8.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5))
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("LIVE TELEMETRY", fontWeight = FontWeight.Bold, color = Color.DarkGray)
                Spacer(modifier = Modifier.height(12.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Active Nodes:", fontWeight = FontWeight.Medium)
                    Text(activeNodes, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("API Latency:", fontWeight = FontWeight.Medium)
                    Text(apiLatency, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
