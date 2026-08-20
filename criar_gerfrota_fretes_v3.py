#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================
GERADOR DO PROJETO GerFrota Fretes v1.0 - NOVO APP
=============================================================
App Android para gestão de fretes com todas as funcionalidades
USO: python3 criar_gerfrota_fretes_v3.py
=============================================================
"""
import os
import sys

PROJETO = "GerFrotaFretesApp"
A = {}

# 1. settings.gradle.kts
A["settings.gradle.kts"] = r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://repo1.maven.org/maven2/") }
    }
}
rootProject.name = "GerFrotaFretes"
include(":app")
'''

# 2. build.gradle.kts (raiz)
A["build.gradle.kts"] = r'''plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
    id("com.google.devtools.ksp") version "1.9.20-1.0.14" apply false
}
'''

# 3. gradle.properties
A["gradle.properties"] = r'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
'''

# 4. app/build.gradle.kts - COM SIGNING CONFIG NO RELEASE (OPÇÃO B)
A["app/build.gradle.kts"] = r'''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.devtools.ksp")
}

android {
    namespace = "com.gerfrota.fretes.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.gerfrota.fretes.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.4" }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }

    buildTypes {
        release {
            isMinifyEnabled = false
            isShrinkResources = false
            signingConfig = signingConfigs.getByName("debug")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    
    packagingOptions {
        resources {
            pickFirsts += listOf(
                "META-INF/DEPENDENCIES",
                "META-INF/LICENSE",
                "META-INF/LICENSE.txt",
                "META-INF/NOTICE",
                "META-INF/NOTICE.txt"
            )
        }
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.7.7")
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    implementation("androidx.datastore:datastore-preferences:1.0.0")
    implementation("com.google.api-client:google-api-client-android:2.2.0") {
        exclude(group = "org.apache.httpcomponents")
    }
    implementation("com.google.apis:google-api-services-drive:v3-rev20220815-2.0.0") {
        exclude(group = "org.apache.httpcomponents")
    }
    implementation("com.google.auth:google-auth-library-oauth2-http:1.19.0")
    implementation("com.google.android.gms:play-services-auth:21.0.0")
    
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2024.02.00"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
'''

# 5. AndroidManifest.xml
A["app/src/main/AndroidManifest.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.RECORD_AUDIO"/>
    <uses-permission android:name="android.permission.GET_ACCOUNTS"/>

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GerFrotaFretes">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.GerFrotaFretes">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths"/>
        </provider>
    </application>
</manifest>
'''

# 6. Theme.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/theme/Theme.kt"] = r'''package com.gerfrota.fretes.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

object GerFrotaColors {
    val Primary = Color(0xFF102A43)
    val Secondary = Color(0xFF0F766E)
    val Tertiary = Color(0xFFF59E0B)
    val Error = Color(0xFFB42318)
    val Surface = Color(0xFFF8FAFC)
    val Card = Color(0xFFFFFFFF)
    val Border = Color(0xFFE2E8F0)
    
    val DarkPrimary = Color(0xFF1E3A5F)
    val DarkSecondary = Color(0xFF14B8A6)
    val DarkSurface = Color(0xFF0F172A)
    val DarkCard = Color(0xFF1E293B)
    val DarkBorder = Color(0xFF334155)
}

private val DarkColorScheme = darkColorScheme(
    primary = GerFrotaColors.DarkPrimary,
    secondary = GerFrotaColors.DarkSecondary,
    tertiary = GerFrotaColors.Tertiary,
    error = GerFrotaColors.Error,
    surface = GerFrotaColors.DarkSurface,
    background = Color(0xFF020617)
)

private val LightColorScheme = lightColorScheme(
    primary = GerFrotaColors.Primary,
    secondary = GerFrotaColors.Secondary,
    tertiary = GerFrotaColors.Tertiary,
    error = GerFrotaColors.Error,
    surface = GerFrotaColors.Surface,
    background = Color(0xFFFFFFFF)
)

@Composable
fun GerFrotaTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    MaterialTheme(colorScheme = colorScheme, content = content)
}
'''

# 7. Type.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/theme/Type.kt"] = r'''package com.gerfrota.fretes.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val GerFrotaTypography = Typography(
    headlineLarge = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Bold, fontSize = 28.sp, lineHeight = 36.sp),
    headlineMedium = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Bold, fontSize = 24.sp, lineHeight = 32.sp),
    titleLarge = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.SemiBold, fontSize = 20.sp, lineHeight = 28.sp),
    titleMedium = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Medium, fontSize = 16.sp, lineHeight = 24.sp),
    bodyLarge = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Normal, fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Normal, fontSize = 14.sp, lineHeight = 20.sp),
    labelLarge = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Medium, fontSize = 14.sp, lineHeight = 20.sp)
)
'''

# 8. Shape.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/theme/Shape.kt"] = r'''package com.gerfrota.fretes.app.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Shapes
import androidx.compose.ui.unit.dp

val GerFrotaShapes = Shapes(
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp)
)
'''

# 9. PlacaEntity.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/PlacaEntity.kt"] = r'''package com.gerfrota.fretes.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "placas")
data class PlacaEntity(
    @PrimaryKey val placa: String,
    val ativa: Boolean = true,
    val dataCadastro: Long = System.currentTimeMillis()
)

object PlacasPadrao {
    val lista = listOf("MLH 6C45", "QEW 8G04", "IWU 3D11", "ITL 4F00", "IXL 6H19")
}
'''

# 10. FreteEntity.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/FreteEntity.kt"] = r'''package com.gerfrota.fretes.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "fretes")
data class FreteEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val data: String,
    val placa: String,
    val valorFrete: Double,
    val adiantamento: Double,
    val formaPgtoAdiant: String,
    val saldoFrete: Double,
    val formaPgtoSaldo: String,
    val recebido: Boolean,
    val transportadora: String,
    val origem: String,
    val destino: String,
    val syncStatus: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis(),
    val recebidoEm: Long? = null,
    val observacao: String? = null,
    val isDraft: Boolean = false
)

object FormasPagamento {
    val opcoes = listOf(
        "PIX PF", "PIX VITALI", "PIX COOP", "PIX MOTORISTA",
        "DEP. CTA. PF", "DEP. CTA. VITALI", "DEP. CTA. COOP",
        "DEP. CTA MOTORISTA", "CHEQUE"
    )
}

data class PlacaResumo(
    val placa: String,
    val totalFretes: Int,
    val totalValor: Double,
    val totalAdiantamento: Double,
    val totalSaldo: Double,
    val totalRecebido: Double
)

data class ResumoFormaPagto(
    val formaPagto: String,
    val totalFretes: Int,
    val totalValor: Double
)
'''

# 11. PlacaDao.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/PlacaDao.kt"] = r'''package com.gerfrota.fretes.app.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface PlacaDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insert(placa: PlacaEntity)
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertAll(placas: List<PlacaEntity>)
    @Update suspend fun update(placa: PlacaEntity)
    @Delete suspend fun delete(placa: PlacaEntity)
    
    @Query("DELETE FROM placas WHERE placa = :placa") suspend fun deleteByPlaca(placa: String)
    @Query("SELECT * FROM placas WHERE ativa = 1 ORDER BY dataCadastro DESC") fun getAllAtivas(): Flow<List<PlacaEntity>>
    @Query("SELECT * FROM placas ORDER BY dataCadastro DESC") fun getAll(): Flow<List<PlacaEntity>>
    @Query("SELECT placa FROM placas WHERE ativa = 1 ORDER BY placa ASC") fun getAllPlacasAtivas(): Flow<List<String>>
    @Query("SELECT COUNT(*) FROM placas WHERE placa = :placa") suspend fun countByPlaca(placa: String): Int
    @Query("UPDATE placas SET ativa = 0 WHERE placa = :placa") suspend fun desativar(placa: String)
    @Query("UPDATE placas SET ativa = 1 WHERE placa = :placa") suspend fun ativar(placa: String)
}
'''

# 12. FreteDao.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/FreteDao.kt"] = r'''package com.gerfrota.fretes.app.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface FreteDao {
    @Insert suspend fun insert(frete: FreteEntity)
    @Insert suspend fun insertAll(fretes: List<FreteEntity>)
    @Update suspend fun update(frete: FreteEntity)
    @Delete suspend fun delete(frete: FreteEntity)
    @Query("DELETE FROM fretes") suspend fun deleteAll()
    @Query("SELECT COUNT(*) FROM fretes") suspend fun count(): Int
    
    @Query("SELECT * FROM fretes ORDER BY id DESC") fun getAll(): Flow<List<FreteEntity>>
    @Query("SELECT * FROM fretes WHERE id = :id") suspend fun getById(id: Long): FreteEntity?
    @Query("SELECT * FROM fretes WHERE recebido = 0 ORDER BY id DESC") fun getNaoRecebidos(): Flow<List<FreteEntity>>
    @Query("SELECT * FROM fretes WHERE transportadora = :transportadora ORDER BY id DESC") fun getPorTransportadora(transportadora: String): Flow<List<FreteEntity>>
    @Query("SELECT * FROM fretes WHERE placa = :placa ORDER BY id DESC") fun getPorPlaca(placa: String): Flow<List<FreteEntity>>
    
    @Query("SELECT transportadora, SUM(saldoFrete) as total FROM fretes WHERE recebido = 0 GROUP BY transportadora ORDER BY total DESC")
    fun saldoPorTransportadora(): Flow<List<SaldoTransportadora>>
    
    @Query("SELECT SUM(saldoFrete) FROM fretes WHERE recebido = 0") fun saldoTotalAReceber(): Flow<Double?>
    @Query("SELECT SUM(adiantamento) FROM fretes") fun totalAdiantamentos(): Flow<Double?>
    
    @Query("""
        SELECT placa, COUNT(*) as totalFretes, SUM(valorFrete) as totalValor, SUM(adiantamento) as totalAdiantamento,
        SUM(saldoFrete) as totalSaldo, SUM(CASE WHEN recebido = 1 THEN saldoFrete ELSE 0 END) as totalRecebido
        FROM fretes GROUP BY placa ORDER BY totalSaldo DESC
    """)
    fun resumoPorPlaca(): Flow<List<PlacaResumo>>
    
    @Query("SELECT * FROM fretes WHERE placa = :placa ORDER BY id DESC") fun getFretesPorPlaca(placa: String): Flow<List<FreteEntity>>
    @Query("SELECT DISTINCT transportadora FROM fretes ORDER BY transportadora") fun getAllTransportadoras(): Flow<List<String>>
    
    @Query("""
        SELECT formaPgtoAdiant as formaPagto, COUNT(*) as totalFretes, SUM(adiantamento) as totalValor
        FROM fretes WHERE adiantamento > 0 GROUP BY formaPgtoAdiant ORDER BY totalValor DESC
    """)
    fun resumoAdiantamentoPorForma(): Flow<List<ResumoFormaPagto>>
    
    @Query("""
        SELECT formaPgtoSaldo as formaPagto, COUNT(*) as totalFretes, SUM(saldoFrete) as totalValor
        FROM fretes WHERE saldoFrete > 0 AND recebido = 0 GROUP BY formaPgtoSaldo ORDER BY totalValor DESC
    """)
    fun resumoSaldoPorForma(): Flow<List<ResumoFormaPagto>>
    
    @Query("SELECT * FROM fretes WHERE formaPgtoAdiant = :forma ORDER BY id DESC") fun getFretesPorFormaAdiant(forma: String): Flow<List<FreteEntity>>
    @Query("SELECT * FROM fretes WHERE formaPgtoSaldo = :forma AND recebido = 0 ORDER BY id DESC") fun getFretesPorFormaSaldo(forma: String): Flow<List<FreteEntity>>
    @Query("SELECT * FROM fretes WHERE data LIKE :mes ORDER BY id DESC") fun getFretesPorMes(mes: String): Flow<List<FreteEntity>>
    
    @Query("SELECT COUNT(*) FROM fretes WHERE recebido = 1 AND data LIKE :mes") suspend fun countRecebidosPorMes(mes: String): Int
    @Query("SELECT COUNT(*) FROM fretes WHERE data LIKE :mes") suspend fun countFretesPorMes(mes: String): Int
    
    @Query("SELECT * FROM fretes WHERE isDraft = 1 ORDER BY updatedAt DESC LIMIT 1") fun getRascunho(): Flow<FreteEntity?>
    @Query("DELETE FROM fretes WHERE isDraft = 1") suspend fun deleteRascunhos()
}

data class SaldoTransportadora(val transportadora: String, val total: Double)
'''

# 13. AppDatabase.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/AppDatabase.kt"] = r'''package com.gerfrota.fretes.app.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [FreteEntity::class, PlacaEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun freteDao(): FreteDao
    abstract fun placaDao(): PlacaDao

    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null

        fun get(context: Context): AppDatabase =
            INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(context.applicationContext, AppDatabase::class.java, "gerfrota.db")
                    .fallbackToDestructiveMigration()
                    .build().also { INSTANCE = it }
            }
    }
}
'''

# 14. Repository.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/Repository.kt"] = r'''package com.gerfrota.fretes.app.data

import kotlinx.coroutines.flow.Flow

class Repository(private val dao: FreteDao, private val placaDao: PlacaDao) {
    val fretes: Flow<List<FreteEntity>> = dao.getAll()
    val fretesNaoRecebidos: Flow<List<FreteEntity>> = dao.getNaoRecebidos()
    val saldoPorTransportadora: Flow<List<SaldoTransportadora>> = dao.saldoPorTransportadora()
    val saldoTotal: Flow<Double?> = dao.saldoTotalAReceber()
    val totalAdiantamentos: Flow<Double?> = dao.totalAdiantamentos()
    val resumoPorPlaca: Flow<List<PlacaResumo>> = dao.resumoPorPlaca()
    val resumoAdiantamentoPorForma: Flow<List<ResumoFormaPagto>> = dao.resumoAdiantamentoPorForma()
    val resumoSaldoPorForma: Flow<List<ResumoFormaPagto>> = dao.resumoSaldoPorForma()
    
    val placasAtivas: Flow<List<PlacaEntity>> = placaDao.getAllAtivas()
    val placasLista: Flow<List<String>> = placaDao.getAllPlacasAtivas()
    val todasPlacas: Flow<List<PlacaEntity>> = placaDao.getAll()
    val transportadoras: Flow<List<String>> = dao.getAllTransportadoras()
    val rascunho: Flow<FreteEntity?> = dao.getRascunho()

    suspend fun insert(f: FreteEntity) = dao.insert(f)
    suspend fun insertAll(fretes: List<FreteEntity>) = dao.insertAll(fretes)
    suspend fun update(f: FreteEntity) = dao.update(f)
    suspend fun delete(f: FreteEntity) = dao.delete(f)
    suspend fun deleteAll() = dao.deleteAll()
    suspend fun count(): Int = dao.count()
    suspend fun getById(id: Long): FreteEntity? = dao.getById(id)
    suspend fun countRecebidosPorMes(mes: String): Int = dao.countRecebidosPorMes(mes)
    suspend fun countFretesPorMes(mes: String): Int = dao.countFretesPorMes(mes)
    suspend fun deleteRascunhos() = dao.deleteRascunhos()

    fun fretesPorPlaca(placa: String): Flow<List<FreteEntity>> = dao.getFretesPorPlaca(placa)
    fun fretesPorTransportadora(transportadora: String): Flow<List<FreteEntity>> = dao.getPorTransportadora(transportadora)
    fun fretesPorFormaAdiant(forma: String): Flow<List<FreteEntity>> = dao.getFretesPorFormaAdiant(forma)
    fun fretesPorFormaSaldo(forma: String): Flow<List<FreteEntity>> = dao.getFretesPorFormaSaldo(forma)
    fun fretesPorMes(mes: String): Flow<List<FreteEntity>> = dao.getFretesPorMes(mes)

    suspend fun insertPlaca(placa: PlacaEntity) = placaDao.insert(placa)
    suspend fun insertPlacas(placas: List<PlacaEntity>) = placaDao.insertAll(placas)
    suspend fun updatePlaca(placa: PlacaEntity) = placaDao.update(placa)
    suspend fun deletePlaca(placa: PlacaEntity) = placaDao.delete(placa)
    suspend fun deletePlacaByNome(placa: String) = placaDao.deleteByPlaca(placa)
    suspend fun placaExiste(placa: String): Boolean = placaDao.countByPlaca(placa) > 0
    suspend fun desativarPlaca(placa: String) = placaDao.desativar(placa)
    suspend fun ativarPlaca(placa: String) = placaDao.ativar(placa)
}
'''

# 15. AuthManager.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/AuthManager.kt"] = r'''package com.gerfrota.fretes.app.data

import android.content.Context
import android.content.SharedPreferences
import java.security.MessageDigest

object AuthManager {
    private const val PREFS = "gerfrota_auth"
    private fun prefs(ctx: Context): SharedPreferences = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    private fun hash(password: String): String {
        val md = MessageDigest.getInstance("SHA-256")
        return md.digest(password.toByteArray(Charsets.UTF_8)).joinToString("") { "%02x".format(it) }
    }

    fun registrar(ctx: Context, email: String, password: String): Boolean {
        if (email.isBlank() || password.length < 4) return false
        prefs(ctx).edit().apply {
            putString("email", email.trim().lowercase())
            putString("pass_hash", hash(password))
            putBoolean("logged", true)
            apply()
        }
        return true
    }

    fun login(ctx: Context, email: String, password: String): LoginResult {
        val p = prefs(ctx)
        val savedEmail = p.getString("email", null)
        val savedHash = p.getString("pass_hash", null)

        if (savedEmail == null || savedHash == null) return LoginResult.NOT_REGISTERED
        if (savedEmail != email.trim().lowercase()) return LoginResult.WRONG_EMAIL
        if (savedHash != hash(password)) return LoginResult.WRONG_PASSWORD

        p.edit().putBoolean("logged", true).apply()
        return LoginResult.SUCCESS
    }

    fun logout(ctx: Context) { prefs(ctx).edit().putBoolean("logged", false).apply() }
    fun isLogged(ctx: Context): Boolean = prefs(ctx).getBoolean("logged", false)
    fun getEmail(ctx: Context): String? = prefs(ctx).getString("email", null)
    fun isRegistered(ctx: Context): Boolean = prefs(ctx).contains("email")
}

enum class LoginResult { SUCCESS, WRONG_EMAIL, WRONG_PASSWORD, NOT_REGISTERED }
'''

# 16. LocalBackupManager.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/LocalBackupManager.kt"] = r'''package com.gerfrota.fretes.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

object LocalBackupManager {
    suspend fun criarBackupLocal(context: Context, fretes: List<FreteEntity>): Pair<Boolean, String> = withContext(Dispatchers.IO) {
        runCatching {
            val fileName = "gerfrota_backup_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale("pt", "BR")).format(Date())}.json"
            val backupDir = File(context.filesDir, "backups").apply { if (!exists()) mkdirs() }
            val backupFile = File(backupDir, fileName)
            
            val jsonArray = JSONArray()
            fretes.forEach { f ->
                jsonArray.put(JSONObject().apply {
                    put("id", f.id); put("data", f.data); put("placa", f.placa); put("valorFrete", f.valorFrete)
                    put("adiantamento", f.adiantamento); put("formaPgtoAdiant", f.formaPgtoAdiant); put("saldoFrete", f.saldoFrete)
                    put("formaPgtoSaldo", f.formaPgtoSaldo); put("recebido", f.recebido); put("transportadora", f.transportadora)
                    put("origem", f.origem); put("destino", f.destino); put("syncStatus", f.syncStatus)
                    put("createdAt", f.createdAt); put("updatedAt", f.updatedAt); put("recebidoEm", f.recebidoEm)
                    put("observacao", f.observacao); put("isDraft", f.isDraft)
                })
            }
            backupFile.writeText(jsonArray.toString(2))
            Pair(true, backupFile.absolutePath)
        }.getOrElse { Pair(false, "Erro: ${it.message}") }
    }

    suspend fun restaurarBackupLocal(context: Context, filePath: String): Pair<Boolean, List<FreteEntity>> = withContext(Dispatchers.IO) {
        runCatching {
            val file = File(filePath)
            if (!file.exists()) return@withContext Pair(false, emptyList())
            
            val jsonArray = JSONArray(file.readText())
            val fretes = mutableListOf<FreteEntity>()
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                fretes.add(FreteEntity(
                    id = obj.optLong("id", 0), data = obj.optString("data", ""), placa = obj.optString("placa", ""),
                    valorFrete = obj.optDouble("valorFrete", 0.0), adiantamento = obj.optDouble("adiantamento", 0.0),
                    formaPgtoAdiant = obj.optString("formaPgtoAdiant", ""), saldoFrete = obj.optDouble("saldoFrete", 0.0),
                    formaPgtoSaldo = obj.optString("formaPgtoSaldo", ""), recebido = obj.optBoolean("recebido", false),
                    transportadora = obj.optString("transportadora", ""), origem = obj.optString("origem", ""),
                    destino = obj.optString("destino", ""), syncStatus = obj.optInt("syncStatus", 0),
                    createdAt = obj.optLong("createdAt", System.currentTimeMillis()),
                    updatedAt = obj.optLong("updatedAt", System.currentTimeMillis()),
                    recebidoEm = if (obj.has("recebidoEm") && !obj.isNull("recebidoEm")) obj.getLong("recebidoEm") else null,
                    observacao = if (obj.has("observacao") && !obj.isNull("observacao")) obj.getString("observacao") else null,
                    isDraft = obj.optBoolean("isDraft", false)
                ))
            }
            Pair(true, fretes.toList())
        }.getOrElse { Pair(false, emptyList()) }
    }
}
'''

# 17. PreferencesManager.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/PreferencesManager.kt"] = r'''package com.gerfrota.fretes.app.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "gerfrota_prefs")

object PreferencesManager {
    object Keys {
        val FILTRO_PERIODO = stringPreferencesKey("filtro_periodo")
        val FILTRO_PLACA = stringPreferencesKey("filtro_placa")
        val FILTRO_STATUS = stringPreferencesKey("filtro_status")
        val FILTRO_TRANSPORTADORA = stringPreferencesKey("filtro_transportadora")
        val ULTIMO_BACKUP = longPreferencesKey("ultimo_backup")
        val CONTA_DRIVE = stringPreferencesKey("conta_drive")
    }

    suspend fun saveFiltroPeriodo(context: Context, periodo: String) { context.dataStore.edit { it[Keys.FILTRO_PERIODO] = periodo } }
    fun getFiltroPeriodo(context: Context): Flow<String?> = context.dataStore.data.map { it[Keys.FILTRO_PERIODO] }
    
    suspend fun saveFiltroPlaca(context: Context, placa: String) { context.dataStore.edit { it[Keys.FILTRO_PLACA] = placa } }
    fun getFiltroPlaca(context: Context): Flow<String?> = context.dataStore.data.map { it[Keys.FILTRO_PLACA] }
    
    suspend fun saveFiltroStatus(context: Context, status: String) { context.dataStore.edit { it[Keys.FILTRO_STATUS] = status } }
    fun getFiltroStatus(context: Context): Flow<String?> = context.dataStore.data.map { it[Keys.FILTRO_STATUS] }
    
    suspend fun saveFiltroTransportadora(context: Context, transportadora: String) { context.dataStore.edit { it[Keys.FILTRO_TRANSPORTADORA] = transportadora } }
    fun getFiltroTransportadora(context: Context): Flow<String?> = context.dataStore.data.map { it[Keys.FILTRO_TRANSPORTADORA] }
    
    suspend fun saveUltimoBackup(context: Context, timestamp: Long) { context.dataStore.edit { it[Keys.ULTIMO_BACKUP] = timestamp } }
    fun getUltimoBackup(context: Context): Flow<Long?> = context.dataStore.data.map { it[Keys.ULTIMO_BACKUP] }
    
    suspend fun saveContaDrive(context: Context, conta: String) { context.dataStore.edit { it[Keys.CONTA_DRIVE] = conta } }
    fun getContaDrive(context: Context): Flow<String?> = context.dataStore.data.map { it[Keys.CONTA_DRIVE] }
}
'''

# 18. MoneyFormatter.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/MoneyFormatter.kt"] = r'''package com.gerfrota.fretes.app.ui

import java.text.NumberFormat
import java.util.Locale

object MoneyFormatter {
    private val format = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
    
    fun format(value: Double): String = format.format(value)
    
    fun parse(text: String): Double {
        val cleaned = text.replace("R$", "").replace(".", "").replace(",", ".").trim()
        return cleaned.toDoubleOrNull() ?: 0.0
    }
    
    fun applyMask(text: String): String {
        val digits = text.filter { it.isDigit() }
        val value = digits.toDoubleOrNull()?.div(100) ?: 0.0
        return format.format(value)
    }
}
'''

# 19. VoiceInputHelper.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/VoiceInputHelper.kt"] = r'''package com.gerfrota.fretes.app.ui

import android.content.Intent
import android.speech.RecognizerIntent
import java.util.Locale

object VoiceInputHelper {
    fun createIntent(): Intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale("pt", "BR"))
        putExtra(RecognizerIntent.EXTRA_PROMPT, "Fale o valor...")
        putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
    }

    fun parseNumber(text: String): String {
        val cleaned = text.lowercase(Locale("pt","BR"))
            .replace("reais", "").replace("real", "")
            .replace("vírgula", ",").replace("virgula", ",")
            .replace("ponto", ".").trim()
        val regex = Regex("[0-9]+([.,][0-9]+)?")
        return regex.find(cleaned)?.value ?: cleaned
    }
}
'''

# 20. PdfExporter.kt
A["app/src/main/java/com/gerfrota/fretes/app/data/PdfExporter.kt"] = r'''package com.gerfrota.fretes.app.data

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import android.net.Uri
import androidx.core.content.FileProvider
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.text.NumberFormat
import java.text.SimpleDateFormat
import java.util.*

object PdfExporter {
    data class PdfResult(val success: Boolean, val message: String, val uri: Uri? = null)

    suspend fun exportar(context: Context, fretes: List<FreteEntity>, titulo: String = "Relatório de Fretes", periodo: String = ""): PdfResult = withContext(Dispatchers.IO) {
        runCatching {
            val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
            val df = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("pt", "BR"))
            val pdf = PdfDocument()
            
            val pageW = 595; val pageH = 842; val margin = 30f
            val pTitle = Paint().apply { color = Color.parseColor("#102A43"); textSize = 20f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pSub = Paint().apply { color = Color.parseColor("#0F766E"); textSize = 11f; isAntiAlias = true }
            val pHead = Paint().apply { color = Color.WHITE; textSize = 9f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pCell = Paint().apply { color = Color.BLACK; textSize = 8f; isAntiAlias = true }
            val pBold = Paint().apply { color = Color.BLACK; textSize = 8f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pBgH = Paint().apply { color = Color.parseColor("#0F766E") }
            val pBgA = Paint().apply { color = Color.parseColor("#F5F5F5") }
            val pBord = Paint().apply { color = Color.parseColor("#BDBDBD"); style = Paint.Style.STROKE; strokeWidth = 0.5f }
            val pTot = Paint().apply { color = Color.parseColor("#102A43"); textSize = 12f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }

            val colX = floatArrayOf(margin, margin + 50, margin + 100, margin + 180, margin + 290, margin + 340, margin + 390, margin + 440, margin + 485)
            val headers = arrayOf("Data", "Placa", "Transportadora", "Rota", "Valor", "Adiant.", "Saldo", "Status")
            val rowH = 16f; val headerY = 100f; val rowsPerPage = 40
            
            val totalPag = kotlin.math.max(1, kotlin.math.ceil(fretes.size.toDouble() / rowsPerPage).toInt())
            var tV = 0.0; var tA = 0.0; var tS = 0.0; var tRecebido = 0.0

            for (pg in 0 until totalPag) {
                val page = pdf.startPage(PdfDocument.PageInfo.Builder(pageW, pageH, pg).create())
                val c = page.canvas
                
                c.drawText(titulo, margin, 40f, pTitle)
                if (periodo.isNotEmpty()) c.drawText("Período: $periodo", margin, 58f, pSub)
                c.drawText("Gerado em ${df.format(Date())} - Página ${pg + 1} de $totalPag", margin, 72f, pSub)
                c.drawLine(margin, 82f, pageW - margin, 82f, pBord)
                
                c.drawRect(margin, headerY - 12f, pageW - margin, headerY + 4f, pBgH)
                headers.forEachIndexed { i, h -> c.drawText(h, colX[i], headerY, pHead) }
                
                val ini = pg * rowsPerPage
                val fim = kotlin.math.min(ini + rowsPerPage, fretes.size)
                var y = headerY + rowH
                
                for (idx in ini until fim) {
                    val f = fretes[idx]
                    if ((idx - ini) % 2 == 1) c.drawRect(margin, y - 10f, pageW - margin, y + 6f, pBgA)
                    
                    c.drawText(f.data, colX[0], y, pCell)
                    c.drawText(f.placa, colX[1], y, pCell)
                    c.drawText(f.transportadora.ifBlank { "-" }, colX[2], y, pCell)
                    c.drawText("${f.origem.ifBlank{"-"}} -> ${f.destino.ifBlank{"-"}}".take(22), colX[3], y, pCell)
                    c.drawText(nf.format(f.valorFrete), colX[4], y, pCell)
                    c.drawText(nf.format(f.adiantamento), colX[5], y, pCell)
                    c.drawText(nf.format(f.saldoFrete), colX[6], y, if (f.saldoFrete > 0) pBold else pCell)
                    c.drawText(if (f.recebido) "Recebido" else "Pendente", colX[7], y, if (f.recebido) Paint().apply { color = Color.GREEN; textSize = 8f } else Paint().apply { color = Color.RED; textSize = 8f })
                    
                    tV += f.valorFrete; tA += f.adiantamento; tS += f.saldoFrete
                    if (f.recebido) tRecebido += f.saldoFrete
                    y += rowH
                }
                c.drawRect(margin, headerY - 12f, pageW - margin, y, pBord)
                
                if (pg == totalPag - 1) {
                    val ty = y + 25f
                    c.drawText("RESUMO:", margin, ty, pTot)
                    c.drawText("Total Fretes: ${nf.format(tV)}", margin, ty + 18f, pBold)
                    c.drawText("Total Adiantamentos: ${nf.format(tA)}", margin + 150f, ty + 18f, pBold)
                    c.drawText("Total Recebido: ${nf.format(tRecebido)}", margin + 320f, ty + 18f, Paint().apply { color = Color.GREEN; textSize = 12f; isAntiAlias = true })
                    c.drawText("Saldo a Receber: ${nf.format(tS)}", margin + 320f, ty + 36f, Paint().apply { color = Color.RED; textSize = 12f; isAntiAlias = true })
                    c.drawText("Total de registros: ${fretes.size}", margin, ty + 56f, pSub)
                }
                pdf.finishPage(page)
            }
            
            val fileName = "GerFrota_Relatorio_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale("pt","BR")).format(Date())}.pdf"
            val folder = File(context.filesDir, "relatorios").apply { if (!exists()) mkdirs() }
            val file = File(folder, fileName)
            FileOutputStream(file).use { out -> pdf.writeTo(out) }
            pdf.close()
            
            PdfResult(true, "Relatório gerado!", FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file))
        }.getOrElse { PdfResult(false, "Erro: ${it.message}") }
    }

    suspend fun exportarAdiantamentoPorForma(context: Context, resumo: List<ResumoFormaPagto>, fretes: List<FreteEntity>): PdfResult = withContext(Dispatchers.IO) {
        runCatching {
            val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
            val df = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("pt", "BR"))
            val pdf = PdfDocument()
            
            val pageW = 595; val pageH = 842; val margin = 30f
            val pTitle = Paint().apply { color = Color.parseColor("#102A43"); textSize = 20f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pSub = Paint().apply { color = Color.parseColor("#0F766E"); textSize = 11f; isAntiAlias = true }
            val pHead = Paint().apply { color = Color.WHITE; textSize = 9f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pCell = Paint().apply { color = Color.BLACK; textSize = 8f; isAntiAlias = true }
            val pBold = Paint().apply { color = Color.BLACK; textSize = 8f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pBgH = Paint().apply { color = Color.parseColor("#0F766E") }
            val pBgA = Paint().apply { color = Color.parseColor("#F5F5F5") }
            val pBord = Paint().apply { color = Color.parseColor("#BDBDBD"); style = Paint.Style.STROKE; strokeWidth = 0.5f }
            val pTot = Paint().apply { color = Color.parseColor("#102A43"); textSize = 12f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }

            val colX = floatArrayOf(margin, margin + 60, margin + 120, margin + 200, margin + 280, margin + 360, margin + 440)
            val headers = arrayOf("Data", "Placa", "Transportadora", "Rota", "Forma Pgto", "Valor Adiant.")
            val rowH = 16f; val headerY = 100f; val rowsPerPage = 40
            
            val fretesAdiant = fretes.filter { it.adiantamento > 0 }
            val totalPag = kotlin.math.max(1, kotlin.math.ceil(fretesAdiant.size.toDouble() / rowsPerPage).toInt())
            var tA = 0.0

            for (pg in 0 until totalPag) {
                val page = pdf.startPage(PdfDocument.PageInfo.Builder(pageW, pageH, pg).create())
                val c = page.canvas
                
                c.drawText("Relatório de Adiantamentos por Forma de Pagamento", margin, 40f, pTitle)
                c.drawText("Gerado em ${df.format(Date())} - Página ${pg + 1} de $totalPag", margin, 58f, pSub)
                c.drawLine(margin, 70f, pageW - margin, 70f, pBord)
                
                c.drawRect(margin, headerY - 12f, pageW - margin, headerY + 4f, pBgH)
                headers.forEachIndexed { i, h -> c.drawText(h, colX[i], headerY, pHead) }
                
                val ini = pg * rowsPerPage
                val fim = kotlin.math.min(ini + rowsPerPage, fretesAdiant.size)
                var y = headerY + rowH
                
                for (idx in ini until fim) {
                    val f = fretesAdiant[idx]
                    if ((idx - ini) % 2 == 1) c.drawRect(margin, y - 10f, pageW - margin, y + 6f, pBgA)
                    
                    c.drawText(f.data, colX[0], y, pCell)
                    c.drawText(f.placa, colX[1], y, pCell)
                    c.drawText(f.transportadora.ifBlank { "-" }, colX[2], y, pCell)
                    c.drawText("${f.origem.ifBlank{"-"}} -> ${f.destino.ifBlank{"-"}}".take(18), colX[3], y, pCell)
                    c.drawText(f.formaPgtoAdiant, colX[4], y, pCell)
                    c.drawText(nf.format(f.adiantamento), colX[5], y, pBold)
                    
                    tA += f.adiantamento
                    y += rowH
                }
                c.drawRect(margin, headerY - 12f, pageW - margin, y, pBord)
                
                if (pg == totalPag - 1) {
                    val ty = y + 25f
                    c.drawText("RESUMO POR FORMA DE PAGAMENTO:", margin, ty, pTot)
                    var yPos = ty + 20f
                    resumo.forEach { r -> c.drawText("${r.formaPagto}: ${r.totalFretes}x ${nf.format(r.totalValor)}", margin, yPos, pCell); yPos += 16f }
                    c.drawText("TOTAL GERAL: ${nf.format(tA)}", margin, yPos + 10f, pTot)
                }
                pdf.finishPage(page)
            }
            
            val fileName = "GerFrota_Adiantamentos_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale("pt","BR")).format(Date())}.pdf"
            val folder = File(context.filesDir, "relatorios").apply { if (!exists()) mkdirs() }
            val file = File(folder, fileName)
            FileOutputStream(file).use { out -> pdf.writeTo(out) }
            pdf.close()
            
            PdfResult(true, "Relatório de adiantamentos gerado!", FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file))
        }.getOrElse { PdfResult(false, "Erro: ${it.message}") }
    }

    suspend fun exportarSaldoPorForma(context: Context, resumo: List<ResumoFormaPagto>, fretes: List<FreteEntity>): PdfResult = withContext(Dispatchers.IO) {
        runCatching {
            val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
            val df = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("pt", "BR"))
            val pdf = PdfDocument()
            
            val pageW = 595; val pageH = 842; val margin = 30f
            val pTitle = Paint().apply { color = Color.parseColor("#102A43"); textSize = 20f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pSub = Paint().apply { color = Color.parseColor("#0F766E"); textSize = 11f; isAntiAlias = true }
            val pHead = Paint().apply { color = Color.WHITE; textSize = 9f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pCell = Paint().apply { color = Color.BLACK; textSize = 8f; isAntiAlias = true }
            val pBold = Paint().apply { color = Color.BLACK; textSize = 8f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
            val pBgH = Paint().apply { color = Color.parseColor("#B42318") }
            val pBgA = Paint().apply { color = Color.parseColor("#F5F5F5") }
            val pBord = Paint().apply { color = Color.parseColor("#BDBDBD"); style = Paint.Style.STROKE; strokeWidth = 0.5f }
            val pTot = Paint().apply { color = Color.parseColor("#102A43"); textSize = 12f; isAntiAlias = true; typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }

            val colX = floatArrayOf(margin, margin + 60, margin + 120, margin + 200, margin + 280, margin + 360, margin + 440)
            val headers = arrayOf("Data", "Placa", "Transportadora", "Rota", "Forma Pgto", "Saldo")
            val rowH = 16f; val headerY = 100f; val rowsPerPage = 40
            
            val fretesSaldo = fretes.filter { it.saldoFrete > 0 && !it.recebido }
            val totalPag = kotlin.math.max(1, kotlin.math.ceil(fretesSaldo.size.toDouble() / rowsPerPage).toInt())
            var tS = 0.0

            for (pg in 0 until totalPag) {
                val page = pdf.startPage(PdfDocument.PageInfo.Builder(pageW, pageH, pg).create())
                val c = page.canvas
                
                c.drawText("Relatório de Saldo a Receber por Forma de Pagamento", margin, 40f, pTitle)
                c.drawText("Gerado em ${df.format(Date())} - Página ${pg + 1} de $totalPag", margin, 58f, pSub)
                c.drawLine(margin, 70f, pageW - margin, 70f, pBord)
                
                c.drawRect(margin, headerY - 12f, pageW - margin, headerY + 4f, pBgH)
                headers.forEachIndexed { i, h -> c.drawText(h, colX[i], headerY, pHead) }
                
                val ini = pg * rowsPerPage
                val fim = kotlin.math.min(ini + rowsPerPage, fretesSaldo.size)
                var y = headerY + rowH
                
                for (idx in ini until fim) {
                    val f = fretesSaldo[idx]
                    if ((idx - ini) % 2 == 1) c.drawRect(margin, y - 10f, pageW - margin, y + 6f, pBgA)
                    
                    c.drawText(f.data, colX[0], y, pCell)
                    c.drawText(f.placa, colX[1], y, pCell)
                    c.drawText(f.transportadora.ifBlank { "-" }, colX[2], y, pCell)
                    c.drawText("${f.origem.ifBlank{"-"}} -> ${f.destino.ifBlank{"-"}}".take(18), colX[3], y, pCell)
                    c.drawText(f.formaPgtoSaldo, colX[4], y, pCell)
                    c.drawText(nf.format(f.saldoFrete), colX[5], y, pBold)
                    
                    tS += f.saldoFrete
                    y += rowH
                }
                c.drawRect(margin, headerY - 12f, pageW - margin, y, pBord)
                
                if (pg == totalPag - 1) {
                    val ty = y + 25f
                    c.drawText("RESUMO POR FORMA DE PAGAMENTO:", margin, ty, pTot)
                    var yPos = ty + 20f
                    resumo.forEach { r -> c.drawText("${r.formaPagto}: ${r.totalFretes}x ${nf.format(r.totalValor)}", margin, yPos, pCell); yPos += 16f }
                    c.drawText("TOTAL GERAL A RECEBER: ${nf.format(tS)}", margin, yPos + 10f, pTot)
                }
                pdf.finishPage(page)
            }
            
            val fileName = "GerFrota_Saldo_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale("pt","BR")).format(Date())}.pdf"
            val folder = File(context.filesDir, "relatorios").apply { if (!exists()) mkdirs() }
            val file = File(folder, fileName)
            FileOutputStream(file).use { out -> pdf.writeTo(out) }
            pdf.close()
            
            PdfResult(true, "Relatório de saldo gerado!", FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file))
        }.getOrElse { PdfResult(false, "Erro: ${it.message}") }
    }

    fun compartilharPdf(context: Context, uri: Uri, tipo: String = "whatsapp"): Boolean {
        return try {
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "application/pdf"
                putExtra(Intent.EXTRA_STREAM, uri)
                putExtra(Intent.EXTRA_SUBJECT, "Relatório GerFrota Fretes")
                putExtra(Intent.EXTRA_TEXT, "Segue o relatório de fretes GerFrota.")
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                if (tipo == "whatsapp") setPackage("com.whatsapp")
            }
            context.startActivity(Intent.createChooser(intent, "Compartilhar via..."))
            true
        } catch (e: Exception) { false }
    }
}
'''

# 21. DriveBackupManager.kt
A["app/src/main/java/com/gerfrota/fretes/app/drive/DriveBackupManager.kt"] = r'''package com.gerfrota.fretes.app.drive

import android.accounts.AccountManager
import android.content.Context
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential
import com.google.api.client.http.InputStreamContent
import com.google.api.client.http.javanet.NetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.drive.Drive
import com.google.api.services.drive.DriveScopes
import com.google.api.services.drive.model.File
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.FileInputStream

class DriveBackupManager(private val context: Context) {
    private fun getGoogleAccount(): String? {
        val am = AccountManager.get(context)
        return am.getAccountsByType("com.google").firstOrNull()?.name
    }

    private fun buildDrive(accountEmail: String): Drive {
        val credential = GoogleAccountCredential.usingOAuth2(context, listOf(DriveScopes.DRIVE_FILE)).apply { selectedAccountName = accountEmail }
        return Drive.Builder(NetHttpTransport(), GsonFactory.getDefaultInstance(), credential).setApplicationName("GerFrotaFretes").build()
    }

    suspend fun uploadBackupParaDrive(backupPath: String): BackupDriveResult = withContext(Dispatchers.IO) {
        runCatching {
            val accountEmail = getGoogleAccount() ?: return@withContext BackupDriveResult.Error("Nenhuma conta Google no dispositivo.")
            val drive = buildDrive(accountEmail)
            
            val backupFile = java.io.File(backupPath)
            val fileInputStream = FileInputStream(backupFile)
            val mediaContent = InputStreamContent("application/json", fileInputStream)
            
            val metadata = File().apply { name = "gerfrota_backup_${System.currentTimeMillis()}.json"; mimeType = "application/json" }
            
            val query = "name contains 'gerfrota_backup' and mimeType='application/json' and trashed=false"
            val existing = drive.files().list().setQ(query).setSpaces("drive").setFields("files(id, name)").execute()
            
            if (existing.files.isNullOrEmpty()) {
                drive.files().create(metadata, mediaContent).setFields("id").execute()
            } else {
                drive.files().update(existing.files[0].id, metadata, mediaContent).execute()
            }
            fileInputStream.close()
            
            BackupDriveResult.Sucesso("Backup enviado para Drive ($accountEmail)")
        }.getOrElse { BackupDriveResult.Error("Erro no upload: ${it.message}") }
    }

    suspend fun downloadBackupDoDrive(): BackupDriveResult = withContext(Dispatchers.IO) {
        runCatching {
            val accountEmail = getGoogleAccount() ?: return@withContext BackupDriveResult.Error("Nenhuma conta Google no dispositivo.")
            val drive = buildDrive(accountEmail)
            
            val query = "name contains 'gerfrota_backup' and mimeType='application/json' and trashed=false"
            val files = drive.files().list().setQ(query).setSpaces("drive").setFields("files(id, name)").setOrderBy("createdTime desc").execute()
            
            if (files.files.isNullOrEmpty()) return@withContext BackupDriveResult.Error("Nenhum backup encontrado no Drive.")
            
            val fileId = files.files[0].id
            val inputStream = drive.files().get(fileId).executeMediaAsInputStream()
            
            val backupDir = context.filesDir.resolve("backups").apply { if (!exists()) mkdirs() }
            val backupFile = backupDir.resolve("gerfrota_backup_downloaded.json")
            backupFile.outputStream().use { it.write(inputStream.readBytes()) }
            inputStream.close()
            
            BackupDriveResult.Sucesso("Backup baixado do Drive: ${backupFile.absolutePath}")
        }.getOrElse { BackupDriveResult.Error("Erro no download: ${it.message}") }
    }
}

sealed class BackupDriveResult {
    data class Sucesso(val message: String) : BackupDriveResult()
    data class Error(val message: String) : BackupDriveResult()
}
'''

# 22. LoginScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/LoginScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import android.widget.Toast
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.R
import com.gerfrota.fretes.app.data.AuthManager
import com.gerfrota.fretes.app.data.LoginResult
import com.gerfrota.fretes.app.data.Repository

@Composable
fun LoginScreen(repo: Repository, onLoginSuccess: () -> Unit) {
    val context = LocalContext.current
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var isRegisterMode by remember { mutableStateOf(!AuthManager.isRegistered(context)) }
    var loading by remember { mutableStateOf(false) }

    Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.primary) {
        Column(modifier = Modifier.fillMaxSize().padding(32.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
            Image(painter = painterResource(R.drawable.ic_truck_logo), contentDescription = null, modifier = Modifier.size(140.dp))
            Spacer(Modifier.height(20.dp))
            Text("GerFrota Fretes", fontSize = 30.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onPrimary, textAlign = TextAlign.Center)
            Text(if (isRegisterMode) "Crie sua conta" else "Entre com sua conta", fontSize = 15.sp, color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.85f))
            Spacer(Modifier.height(32.dp))

            Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Column(Modifier.padding(20.dp)) {
                    OutlinedTextField(value = email, onValueChange = { email = it }, label = { Text("E-mail") }, leadingIcon = { Icon(Icons.Default.Email, null) }, modifier = Modifier.fillMaxWidth(), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email), singleLine = true)
                    Spacer(Modifier.height(12.dp))
                    OutlinedTextField(value = password, onValueChange = { password = it }, label = { Text("Senha") }, leadingIcon = { Icon(Icons.Default.Lock, null) }, modifier = Modifier.fillMaxWidth(), visualTransformation = PasswordVisualTransformation(), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password), singleLine = true)
                    
                    if (isRegisterMode) {
                        Spacer(Modifier.height(12.dp))
                        OutlinedTextField(value = confirmPassword, onValueChange = { confirmPassword = it }, label = { Text("Confirmar senha") }, leadingIcon = { Icon(Icons.Default.Lock, null) }, modifier = Modifier.fillMaxWidth(), visualTransformation = PasswordVisualTransformation(), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password), singleLine = true)
                    }
                    
                    Spacer(Modifier.height(20.dp))
                    
                    Button(onClick = {
                        if (loading) return@Button
                        loading = true
                        if (isRegisterMode) {
                            if (password != confirmPassword) { Toast.makeText(context, "As senhas não conferem", Toast.LENGTH_SHORT).show(); loading = false; return@Button }
                            if (AuthManager.registrar(context, email, password)) { Toast.makeText(context, "Conta criada!", Toast.LENGTH_SHORT).show(); onLoginSuccess() }
                            else { Toast.makeText(context, "Preencha e-mail e senha (mín. 4)", Toast.LENGTH_SHORT).show() }
                        } else {
                            when (AuthManager.login(context, email, password)) {
                                LoginResult.SUCCESS -> onLoginSuccess()
                                LoginResult.WRONG_EMAIL -> Toast.makeText(context, "E-mail não cadastrado", Toast.LENGTH_SHORT).show()
                                LoginResult.WRONG_PASSWORD -> Toast.makeText(context, "Senha incorreta", Toast.LENGTH_SHORT).show()
                                LoginResult.NOT_REGISTERED -> { isRegisterMode = true; Toast.makeText(context, "Crie uma conta", Toast.LENGTH_SHORT).show() }
                            }
                        }
                        loading = false
                    }, modifier = Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(12.dp), enabled = !loading) {
                        if (loading) CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                        else Text(if (isRegisterMode) "CRIAR CONTA" else "ENTRAR", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                    
                    if (AuthManager.isRegistered(context)) {
                        Spacer(Modifier.height(8.dp))
                        TextButton(onClick = { isRegisterMode = !isRegisterMode }, modifier = Modifier.fillMaxWidth()) { Text(if (isRegisterMode) "Já tenho conta - Entrar" else "Não tenho conta - Criar agora", fontSize = 13.sp) }
                    }
                }
            }
            Spacer(Modifier.height(16.dp))
            Text("Seus dados ficam salvos no dispositivo", fontSize = 12.sp, color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.7f), textAlign = TextAlign.Center)
        }
    }
}
'''

# 23. MainScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/MainScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.gerfrota.fretes.app.data.Repository

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(repo: Repository, userEmail: String, onLogout: () -> Unit) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    
    val bottomNavItems = listOf(
        BottomNavItem("Início", Icons.Default.Home, "inicio"),
        BottomNavItem("Fretes", Icons.Default.LocalShipping, "fretes"),
        BottomNavItem("Financeiro", Icons.Default.AccountBalanceWallet, "financeiro"),
        BottomNavItem("Mais", Icons.Default.MoreHoriz, "mais")
    )

    Scaffold(
        bottomBar = {
            if (currentRoute !in listOf("novo_frete", "detalhe_frete", "editar_frete", "backup", "placas", "relatorios")) {
                NavigationBar {
                    bottomNavItems.forEach { item ->
                        NavigationBarItem(
                            icon = { Icon(item.icon, contentDescription = item.label) },
                            label = { Text(item.label) },
                            selected = currentRoute == item.route,
                            onClick = { navController.navigate(item.route) { popUpTo("inicio") { saveState = true }; launchSingleTop = true; restoreState = true } }
                        )
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(navController = navController, startDestination = "inicio", modifier = Modifier.padding(innerPadding)) {
            composable("inicio") {
                InicioScreen(
                    repo = repo, userEmail = userEmail,
                    onNavigateToNovoFrete = { navController.navigate("novo_frete") },
                    onNavigateToFretes = { navController.navigate("fretes") },
                    onNavigateToFinanceiro = { navController.navigate("financeiro") },
                    onNavigateToRelatorios = { navController.navigate("relatorios") },
                    onNavigateToPlacas = { navController.navigate("placas") },
                    onNavigateToBackup = { navController.navigate("backup") },
                    onLogout = onLogout
                )
            }
            composable("fretes") {
                FretesScreen(
                    repo = repo,
                    onNavigateToNovoFrete = { navController.navigate("novo_frete") },
                    onNavigateToDetalhe = { freteId -> navController.navigate("detalhe_frete/$freteId") }
                )
            }
            composable("financeiro") {
                FinanceiroScreen(
                    repo = repo,
                    onNavigateToDetalhe = { freteId -> navController.navigate("detalhe_frete/$freteId") }
                )
            }
            composable("mais") {
                MaisScreen(
                    userEmail = userEmail,
                    onNavigateToPlacas = { navController.navigate("placas") },
                    onNavigateToBackup = { navController.navigate("backup") },
                    onNavigateToRelatorios = { navController.navigate("relatorios") },
                    onLogout = onLogout
                )
            }
            composable("novo_frete") { NovoFreteScreen(repo = repo, onBack = { navController.popBackStack() }) }
            composable("detalhe_frete/{freteId}") { backStackEntry ->
                val freteId = backStackEntry.arguments?.getString("freteId")?.toLongOrNull()
                if (freteId != null) DetalheFreteScreen(repo = repo, freteId = freteId, onBack = { navController.popBackStack() }, onEdit = { navController.navigate("editar_frete/$freteId") })
            }
            composable("editar_frete/{freteId}") { backStackEntry ->
                val freteId = backStackEntry.arguments?.getString("freteId")?.toLongOrNull()
                if (freteId != null) EditarFreteScreen(repo = repo, freteId = freteId, onBack = { navController.popBackStack() })
            }
            composable("placas") { PlacasScreen(repo = repo, onBack = { navController.popBackStack() }) }
            composable("backup") { BackupScreen(repo = repo, onBack = { navController.popBackStack() }) }
            composable("relatorios") { RelatoriosScreen(repo = repo, onBack = { navController.popBackStack() }) }
        }
    }
}

data class BottomNavItem(val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector, val route: String)
'''

# 24. InicioScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/InicioScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import java.text.NumberFormat
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InicioScreen(
    repo: Repository, userEmail: String,
    onNavigateToNovoFrete: () -> Unit, onNavigateToFretes: () -> Unit,
    onNavigateToFinanceiro: () -> Unit, onNavigateToRelatorios: () -> Unit,
    onNavigateToPlacas: () -> Unit, onNavigateToBackup: () -> Unit,
    onLogout: () -> Unit
) {
    val fretes by repo.fretes.collectAsState(initial = emptyList())
    val saldoTotal by repo.saldoTotal.collectAsState(initial = 0.0)
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
    val currentMonth = SimpleDateFormat("MM/yyyy", Locale("pt", "BR")).format(Date())
    val fretesDoMes by repo.fretesPorMes(currentMonth).collectAsState(initial = emptyList())
    
    val totalRecebidos = remember(fretesDoMes) { fretesDoMes.count { it.recebido } }
    val fretesNaoRecebidos = fretes.count { !it.recebido }

    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item {
            Column {
                Text("Olá, ${userEmail.split("@").first()}", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = GerFrotaColors.Primary)
                Text("Visão operacional de hoje", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
            }
        }
        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                MetricCard(title = "A receber", value = nf.format(saldoTotal ?: 0.0), subtitle = "Saldo total", icon = Icons.Default.AccountBalanceWallet, modifier = Modifier.weight(1f), onClick = onNavigateToFinanceiro)
                MetricCard(title = "Fretes do mês", value = "${fretesDoMes.size}", subtitle = "Este mês", icon = Icons.Default.LocalShipping, modifier = Modifier.weight(1f), onClick = onNavigateToFretes)
            }
        }
        item {
            MetricCard(title = "Recebidos", value = "$totalRecebidos", subtitle = "No mês", icon = Icons.Default.CheckCircle, modifier = Modifier.fillMaxWidth(), onClick = onNavigateToFretes)
        }
        item { Text("Ações rápidas", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold) }
        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                QuickActionCard(label = "Novo frete", icon = Icons.Default.Add, onClick = onNavigateToNovoFrete, modifier = Modifier.weight(1f))
                QuickActionCard(label = "Fretes", icon = Icons.Default.LocalShipping, onClick = onNavigateToFretes, modifier = Modifier.weight(1f))
                QuickActionCard(label = "Financeiro", icon = Icons.Default.AccountBalanceWallet, onClick = onNavigateToFinanceiro, modifier = Modifier.weight(1f))
                QuickActionCard(label = "Relatórios", icon = Icons.Default.BarChart, onClick = onNavigateToRelatorios, modifier = Modifier.weight(1f))
            }
        }
        if (fretesNaoRecebidos > 0) {
            item {
                PendenciaCard(title = "Pagamentos a vencer", subtitle = "$fretesNaoRecebidos títulos", status = "Em dia", statusColor = GerFrotaColors.Secondary, icon = Icons.Default.CreditCard, onClick = onNavigateToFinanceiro)
            }
        }
        if (fretes.isEmpty()) {
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Surface)) {
                    Column(modifier = Modifier.fillMaxWidth().padding(32.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Default.Inbox, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.Gray)
                        Spacer(Modifier.height(16.dp))
                        Text("Ainda não há fretes", style = MaterialTheme.typography.bodyLarge, color = Color.Gray, textAlign = TextAlign.Center)
                        Text("Cadastre o primeiro frete para acompanhar seus saldos.", style = MaterialTheme.typography.bodyMedium, color = Color.Gray, textAlign = TextAlign.Center)
                    }
                }
            }
        }
    }
}

@Composable
fun MetricCard(title: String, value: String, subtitle: String, icon: androidx.compose.ui.graphics.vector.ImageVector, modifier: Modifier = Modifier, onClick: () -> Unit) {
    Card(modifier = modifier.clickable(onClick = onClick), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Card)) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(icon, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(32.dp))
                Spacer(Modifier.width(12.dp))
                Column {
                    Text(title, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    Text(value, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = GerFrotaColors.Primary)
                }
            }
            Spacer(Modifier.height(8.dp))
            Text(subtitle, style = MaterialTheme.typography.labelMedium, color = GerFrotaColors.Secondary)
        }
    }
}

@Composable
fun QuickActionCard(label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Card(modifier = modifier.clickable(onClick = onClick), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Card)) {
        Column(modifier = Modifier.fillMaxWidth().padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(icon, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(32.dp))
            Spacer(Modifier.height(8.dp))
            Text(label, style = MaterialTheme.typography.labelLarge, textAlign = TextAlign.Center)
        }
    }
}

@Composable
fun PendenciaCard(title: String, subtitle: String, status: String, statusColor: Color, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth().clickable(onClick = onClick), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Card)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, contentDescription = null, tint = GerFrotaColors.Tertiary, modifier = Modifier.size(32.dp))
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Medium)
                Text(subtitle, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
            }
            AssistChip(onClick = {}, label = { Text(status) }, colors = AssistChipDefaults.assistChipColors(containerColor = statusColor.copy(alpha = 0.1f), labelColor = statusColor))
            Spacer(Modifier.width(8.dp))
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
        }
    }
}
'''

# 25. FretesScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/FretesScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.FreteEntity
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import java.text.NumberFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FretesScreen(repo: Repository, onNavigateToNovoFrete: () -> Unit, onNavigateToDetalhe: (Long) -> Unit) {
    val fretes by repo.fretes.collectAsState(initial = emptyList())
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
    var searchQuery by remember { mutableStateOf("") }
    
    val fretesFiltrados = remember(fretes, searchQuery) {
        fretes.filter { searchQuery.isEmpty() || it.placa.contains(searchQuery, ignoreCase = true) || it.transportadora.contains(searchQuery, ignoreCase = true) || it.origem.contains(searchQuery, ignoreCase = true) || it.destino.contains(searchQuery, ignoreCase = true) }
    }

    Scaffold(floatingActionButton = {
        FloatingActionButton(onClick = onNavigateToNovoFrete, containerColor = GerFrotaColors.Secondary) {
            Icon(Icons.Default.Add, contentDescription = "Novo frete")
        }
    }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding)) {
            OutlinedTextField(
                value = searchQuery, onValueChange = { searchQuery = it },
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                placeholder = { Text("Buscar placa, transportadora ou rota") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                trailingIcon = { if (searchQuery.isNotEmpty()) IconButton(onClick = { searchQuery = "" }) { Icon(Icons.Default.Clear, contentDescription = "Limpar") } },
                singleLine = true, shape = RoundedCornerShape(12.dp)
            )
            
            if (fretesFiltrados.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Default.SearchOff, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.Gray)
                        Spacer(Modifier.height(16.dp))
                        Text("Nenhum frete encontrado", style = MaterialTheme.typography.bodyLarge, color = Color.Gray, textAlign = TextAlign.Center)
                    }
                }
            } else {
                LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(fretesFiltrados) { frete -> FreteCard(frete = frete, nf = nf, onClick = { onNavigateToDetalhe(frete.id) }) }
                }
            }
        }
    }
}

@Composable
fun FreteCard(frete: FreteEntity, nf: NumberFormat, onClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth().clickable(onClick = onClick), shape = RoundedCornerShape(12.dp), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Card)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.LocalShipping, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(40.dp))
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(frete.placa, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text("${frete.origem} → ${frete.destino}", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                Text(frete.transportadora, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
                Text(frete.data, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            }
            Column(horizontalAlignment = Alignment.End) {
                AssistChip(onClick = {}, label = { Text(if (frete.recebido) "Recebido" else "Em aberto", fontSize = 12.sp) }, colors = AssistChipDefaults.assistChipColors(containerColor = if (frete.recebido) GerFrotaColors.Secondary.copy(alpha = 0.1f) else GerFrotaColors.Tertiary.copy(alpha = 0.1f), labelColor = if (frete.recebido) GerFrotaColors.Secondary else GerFrotaColors.Tertiary))
                Spacer(Modifier.height(8.dp))
                Text(nf.format(frete.valorFrete), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = GerFrotaColors.Primary)
                if (!frete.recebido && frete.saldoFrete > 0) Text("Saldo: ${nf.format(frete.saldoFrete)}", style = MaterialTheme.typography.bodySmall, color = GerFrotaColors.Error)
            }
        }
    }
}
'''

# 26. FinanceiroScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/FinanceiroScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.data.SaldoTransportadora
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import java.text.NumberFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FinanceiroScreen(repo: Repository, onNavigateToDetalhe: (Long) -> Unit) {
    val saldoTotal by repo.saldoTotal.collectAsState(initial = 0.0)
    val saldoPorTransportadora by repo.saldoPorTransportadora.collectAsState(initial = emptyList())
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))

    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item { Text("Financeiro", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold) }
        item {
            Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Primary)) {
                Column(modifier = Modifier.fillMaxWidth().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("Total a receber", style = MaterialTheme.typography.bodyLarge, color = Color.White.copy(alpha = 0.8f))
                    Spacer(Modifier.height(8.dp))
                    Text(nf.format(saldoTotal ?: 0.0), style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
        }
        item { Text("Por transportadora", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold) }
        items(saldoPorTransportadora) { saldo -> TransportadoraCard(saldo = saldo, nf = nf) }
    }
}

@Composable
fun TransportadoraCard(saldo: SaldoTransportadora, nf: NumberFormat) {
    Card(modifier = Modifier.fillMaxWidth().clickable { }, shape = RoundedCornerShape(12.dp)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.Business, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(40.dp))
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(saldo.transportadora, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Medium)
                Text(nf.format(saldo.total), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = GerFrotaColors.Primary)
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
        }
    }
}
'''

# 27. MaisScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/MaisScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors

@Composable
fun MaisScreen(userEmail: String, onNavigateToPlacas: () -> Unit, onNavigateToBackup: () -> Unit, onNavigateToRelatorios: () -> Unit, onLogout: () -> Unit) {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item {
            Card(modifier = Modifier.fillMaxWidth().clickable { }, shape = RoundedCornerShape(12.dp)) {
                Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Person, contentDescription = null, modifier = Modifier.size(48.dp), tint = GerFrotaColors.Primary)
                    Spacer(Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(userEmail.split("@").first(), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Text(userEmail, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    }
                    Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
                }
            }
        }
        item { Text("Operação", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold) }
        item { MenuItem(icon = Icons.Default.LocalParking, label = "Placas", onClick = onNavigateToPlacas) }
        item { MenuItem(icon = Icons.Default.PictureAsPdf, label = "Relatórios", onClick = onNavigateToRelatorios) }
        item { MenuItem(icon = Icons.Default.CloudUpload, label = "Backup e restauração", onClick = onNavigateToBackup) }
        item {
            OutlinedButton(onClick = onLogout, modifier = Modifier.fillMaxWidth().height(56.dp), colors = ButtonDefaults.outlinedButtonColors(contentColor = GerFrotaColors.Error)) {
                Icon(Icons.Default.Logout, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Sair da conta")
            }
        }
    }
}

@Composable
fun MenuItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, subtitle: String? = null, onClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth().clickable(onClick = onClick), shape = RoundedCornerShape(12.dp)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(32.dp))
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(label, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
                if (subtitle != null) Text(subtitle, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
        }
    }
}
'''

# 28. NovoFreteScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/NovoFreteScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.FreteEntity
import com.gerfrota.fretes.app.data.FormasPagamento
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import kotlinx.coroutines.launch
import java.text.NumberFormat
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NovoFreteScreen(repo: Repository, onBack: () -> Unit) {
    val scope = rememberCoroutineScope()
    var data by remember { mutableStateOf(SimpleDateFormat("dd/MM/yyyy", Locale("pt","BR")).format(Date())) }
    var placa by remember { mutableStateOf("") }
    var transportadora by remember { mutableStateOf("") }
    var origem by remember { mutableStateOf("") }
    var destino by remember { mutableStateOf("") }
    var valorFrete by remember { mutableStateOf("") }
    var adiantamento by remember { mutableStateOf("") }
    var formaPgtoAdiant by remember { mutableStateOf(FormasPagamento.opcoes.first()) }
    var formaPgtoSaldo by remember { mutableStateOf(FormasPagamento.opcoes.first()) }
    var recebido by remember { mutableStateOf(false) }
    var showPlacaDropdown by remember { mutableStateOf(false) }
    var showFormaAdiantDropdown by remember { mutableStateOf(false) }
    var showFormaSaldoDropdown by remember { mutableStateOf(false) }
    var erroAdiantamento by remember { mutableStateOf<String?>(null) }
    
    val placas by repo.placasLista.collectAsState(initial = emptyList())
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
    
    val valorFreteDouble = MoneyFormatter.parse(valorFrete)
    val adiantamentoDouble = MoneyFormatter.parse(adiantamento)
    val saldoFrete = if (recebido) 0.0 else (valorFreteDouble - adiantamentoDouble)

    LaunchedEffect(adiantamentoDouble, valorFreteDouble) {
        if (adiantamentoDouble > valorFreteDouble && valorFreteDouble > 0) erroAdiantamento = "Adiantamento não pode ser maior que o valor do frete"
        else erroAdiantamento = null
    }

    Scaffold(topBar = {
        TopAppBar(title = { Text("Novo Frete") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Voltar") } })
    }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding)) {
            Column(modifier = Modifier.fillMaxWidth().weight(1f).verticalScroll(rememberScrollState()).padding(16.dp)) {
                Text("Dados da viagem", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                
                ExposedDropdownMenuBox(expanded = showPlacaDropdown, onExpandedChange = { showPlacaDropdown = it }) {
                    OutlinedTextField(value = placa, onValueChange = { placa = it }, modifier = Modifier.fillMaxWidth().menuAnchor(), label = { Text("Placa") }, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = showPlacaDropdown) })
                    ExposedDropdownMenu(expanded = showPlacaDropdown, onDismissRequest = { showPlacaDropdown = false }) {
                        placas.forEach { p -> DropdownMenuItem(text = { Text(p) }, onClick = { placa = p; showPlacaDropdown = false }) }
                    }
                }
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(value = transportadora, onValueChange = { transportadora = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Transportadora") })
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(value = origem, onValueChange = { origem = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Origem") })
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(value = destino, onValueChange = { destino = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Destino") })
                
                Spacer(Modifier.height(24.dp))
                Text("Valores", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                
                OutlinedTextField(value = valorFrete, onValueChange = { valorFrete = MoneyFormatter.applyMask(it) }, modifier = Modifier.fillMaxWidth(), label = { Text("Valor do frete") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), leadingIcon = { Text("R$", modifier = Modifier.padding(start = 12.dp)) })
                Spacer(Modifier.height(12.dp))
                
                OutlinedTextField(value = adiantamento, onValueChange = { adiantamento = MoneyFormatter.applyMask(it) }, modifier = Modifier.fillMaxWidth(), label = { Text("Adiantamento") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), leadingIcon = { Text("R$", modifier = Modifier.padding(start = 12.dp)) }, isError = erroAdiantamento != null, supportingText = { val err = erroAdiantamento; if (err != null) Text(err, color = MaterialTheme.colorScheme.error) })
                
                Spacer(Modifier.height(16.dp))
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Secondary.copy(alpha = 0.1f))) {
                    Row(modifier = Modifier.fillMaxWidth().padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Text("Saldo do frete", style = MaterialTheme.typography.titleMedium)
                        Text(nf.format(saldoFrete), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = GerFrotaColors.Secondary)
                    }
                }
                
                Spacer(Modifier.height(24.dp))
                Text("Recebimento", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                
                ExposedDropdownMenuBox(expanded = showFormaAdiantDropdown, onExpandedChange = { showFormaAdiantDropdown = it }) {
                    OutlinedTextField(value = formaPgtoAdiant, onValueChange = {}, modifier = Modifier.fillMaxWidth().menuAnchor(), label = { Text("Forma de pagamento - Adiantamento") }, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = showFormaAdiantDropdown) })
                    ExposedDropdownMenu(expanded = showFormaAdiantDropdown, onDismissRequest = { showFormaAdiantDropdown = false }) {
                        FormasPagamento.opcoes.forEach { forma -> DropdownMenuItem(text = { Text(forma) }, onClick = { formaPgtoAdiant = forma; showFormaAdiantDropdown = false }) }
                    }
                }
                Spacer(Modifier.height(12.dp))
                ExposedDropdownMenuBox(expanded = showFormaSaldoDropdown, onExpandedChange = { showFormaSaldoDropdown = it }) {
                    OutlinedTextField(value = formaPgtoSaldo, onValueChange = {}, modifier = Modifier.fillMaxWidth().menuAnchor(), label = { Text("Forma de pagamento - Saldo") }, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = showFormaSaldoDropdown) })
                    ExposedDropdownMenu(expanded = showFormaSaldoDropdown, onDismissRequest = { showFormaSaldoDropdown = false }) {
                        FormasPagamento.opcoes.forEach { forma -> DropdownMenuItem(text = { Text(forma) }, onClick = { formaPgtoSaldo = forma; showFormaSaldoDropdown = false }) }
                    }
                }
                
                Spacer(Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = recebido, onCheckedChange = { recebido = it })
                    Text("Marcar como recebido", style = MaterialTheme.typography.bodyLarge)
                }
                if (recebido) {
                    Card(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Tertiary.copy(alpha = 0.1f))) {
                        Text("Ao marcar como recebido, o saldo será zerado.", modifier = Modifier.padding(12.dp), style = MaterialTheme.typography.bodyMedium, color = GerFrotaColors.Tertiary)
                    }
                }
            }
            
            Button(onClick = {
                scope.launch {
                    val frete = FreteEntity(data = data, placa = placa, transportadora = transportadora, origem = origem, destino = destino, valorFrete = valorFreteDouble, adiantamento = adiantamentoDouble, formaPgtoAdiant = formaPgtoAdiant, saldoFrete = saldoFrete, formaPgtoSaldo = formaPgtoSaldo, recebido = recebido)
                    repo.insert(frete)
                    onBack()
                }
            }, modifier = Modifier.fillMaxWidth().padding(16.dp), enabled = valorFreteDouble > 0 && erroAdiantamento == null) {
                Text("Salvar Frete")
            }
        }
    }
}
'''

# 29. DetalheFreteScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/DetalheFreteScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import kotlinx.coroutines.launch
import java.text.NumberFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetalheFreteScreen(repo: Repository, freteId: Long, onBack: () -> Unit, onEdit: () -> Unit) {
    val scope = rememberCoroutineScope()
    val fretes by repo.fretes.collectAsState(initial = emptyList())
    val freteAtual = fretes.find { it.id == freteId }
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
    var showConfirmDialog by remember { mutableStateOf(false) }

    if (freteAtual == null) { Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }; return }

    Scaffold(topBar = {
        TopAppBar(title = { Text("Detalhe do Frete") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Voltar") } }, actions = { IconButton(onClick = onEdit) { Icon(Icons.Default.Edit, contentDescription = "Editar") } })
    }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = if (freteAtual.recebido) GerFrotaColors.Secondary.copy(alpha = 0.1f) else GerFrotaColors.Tertiary.copy(alpha = 0.1f))) {
                Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(if (freteAtual.recebido) Icons.Default.CheckCircle else Icons.Default.Schedule, contentDescription = null, tint = if (freteAtual.recebido) GerFrotaColors.Secondary else GerFrotaColors.Tertiary, modifier = Modifier.size(32.dp))
                    Spacer(Modifier.width(12.dp))
                    Column {
                        Text(if (freteAtual.recebido) "Recebido" else "Em aberto", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = if (freteAtual.recebido) GerFrotaColors.Secondary else GerFrotaColors.Tertiary)
                        Text(freteAtual.data, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    }
                }
            }
            
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(freteAtual.placa, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.LocationOn, contentDescription = null, tint = Color.Gray)
                        Spacer(Modifier.width(8.dp))
                        Text("${freteAtual.origem} → ${freteAtual.destino}", style = MaterialTheme.typography.bodyLarge)
                    }
                }
            }
            
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Valores", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) { Text("Valor do frete", style = MaterialTheme.typography.bodyLarge); Text(nf.format(freteAtual.valorFrete), style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold) }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) { Text("Adiantamento", style = MaterialTheme.typography.bodyLarge); Text(nf.format(freteAtual.adiantamento), style = MaterialTheme.typography.bodyLarge) }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) { Text("Saldo a receber", style = MaterialTheme.typography.bodyLarge, color = GerFrotaColors.Primary); Text(nf.format(freteAtual.saldoFrete), style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold, color = GerFrotaColors.Secondary) }
                }
            }
            
            if (!freteAtual.recebido) {
                Button(onClick = { showConfirmDialog = true }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = GerFrotaColors.Secondary)) {
                    Icon(Icons.Default.Check, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Marcar como recebido")
                }
            }
        }
    }

    if (showConfirmDialog) {
        AlertDialog(onDismissRequest = { showConfirmDialog = false }, title = { Text("Confirmar recebimento") }, text = { Text("O saldo de ${nf.format(freteAtual.saldoFrete)} será zerado. Deseja continuar?") }, confirmButton = {
            TextButton(onClick = {
                scope.launch {
                    val freteAtualizado = freteAtual.copy(recebido = true, saldoFrete = 0.0, recebidoEm = System.currentTimeMillis(), updatedAt = System.currentTimeMillis())
                    repo.update(freteAtualizado)
                    showConfirmDialog = false
                    onBack()
                }
            }) { Text("Confirmar", color = GerFrotaColors.Secondary) }
        }, dismissButton = { TextButton(onClick = { showConfirmDialog = false }) { Text("Cancelar") } })
    }
}
'''

# 30. EditarFreteScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/EditarFreteScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.FreteEntity
import com.gerfrota.fretes.app.data.FormasPagamento
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import kotlinx.coroutines.launch
import java.text.NumberFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditarFreteScreen(repo: Repository, freteId: Long, onBack: () -> Unit) {
    val scope = rememberCoroutineScope()
    val fretes by repo.fretes.collectAsState(initial = emptyList())
    val frete = fretes.find { it.id == freteId }
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))

    if (frete == null) { Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }; return }

    var placa by remember { mutableStateOf(frete.placa) }
    var transportadora by remember { mutableStateOf(frete.transportadora) }
    var origem by remember { mutableStateOf(frete.origem) }
    var destino by remember { mutableStateOf(frete.destino) }
    var valorFrete by remember { mutableStateOf(MoneyFormatter.format(frete.valorFrete)) }
    var adiantamento by remember { mutableStateOf(MoneyFormatter.format(frete.adiantamento)) }
    var formaPgtoAdiant by remember { mutableStateOf(frete.formaPgtoAdiant) }
    var formaPgtoSaldo by remember { mutableStateOf(frete.formaPgtoSaldo) }
    var recebido by remember { mutableStateOf(frete.recebido) }
    var showFormaAdiantDropdown by remember { mutableStateOf(false) }
    var showFormaSaldoDropdown by remember { mutableStateOf(false) }

    val valorFreteDouble = MoneyFormatter.parse(valorFrete)
    val adiantamentoDouble = MoneyFormatter.parse(adiantamento)
    val saldoFrete = if (recebido) 0.0 else (valorFreteDouble - adiantamentoDouble)

    Scaffold(topBar = { TopAppBar(title = { Text("Editar Frete") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Voltar") } }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedTextField(value = placa, onValueChange = { placa = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Placa") })
            OutlinedTextField(value = transportadora, onValueChange = { transportadora = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Transportadora") })
            OutlinedTextField(value = origem, onValueChange = { origem = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Origem") })
            OutlinedTextField(value = destino, onValueChange = { destino = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Destino") })
            OutlinedTextField(value = valorFrete, onValueChange = { valorFrete = MoneyFormatter.applyMask(it) }, modifier = Modifier.fillMaxWidth(), label = { Text("Valor do frete") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number))
            OutlinedTextField(value = adiantamento, onValueChange = { adiantamento = MoneyFormatter.applyMask(it) }, modifier = Modifier.fillMaxWidth(), label = { Text("Adiantamento") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number))
            
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Secondary.copy(alpha = 0.1f))) {
                Row(modifier = Modifier.fillMaxWidth().padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween) { Text("Saldo do frete", style = MaterialTheme.typography.titleMedium); Text(nf.format(saldoFrete), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = GerFrotaColors.Secondary) }
            }
            
            ExposedDropdownMenuBox(expanded = showFormaAdiantDropdown, onExpandedChange = { showFormaAdiantDropdown = it }) {
                OutlinedTextField(value = formaPgtoAdiant, onValueChange = {}, modifier = Modifier.fillMaxWidth().menuAnchor(), label = { Text("Forma de pagamento - Adiantamento") }, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = showFormaAdiantDropdown) })
                ExposedDropdownMenu(expanded = showFormaAdiantDropdown, onDismissRequest = { showFormaAdiantDropdown = false }) { FormasPagamento.opcoes.forEach { forma -> DropdownMenuItem(text = { Text(forma) }, onClick = { formaPgtoAdiant = forma; showFormaAdiantDropdown = false }) } }
            }
            ExposedDropdownMenuBox(expanded = showFormaSaldoDropdown, onExpandedChange = { showFormaSaldoDropdown = it }) {
                OutlinedTextField(value = formaPgtoSaldo, onValueChange = {}, modifier = Modifier.fillMaxWidth().menuAnchor(), label = { Text("Forma de pagamento - Saldo") }, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = showFormaSaldoDropdown) })
                ExposedDropdownMenu(expanded = showFormaSaldoDropdown, onDismissRequest = { showFormaSaldoDropdown = false }) { FormasPagamento.opcoes.forEach { forma -> DropdownMenuItem(text = { Text(forma) }, onClick = { formaPgtoSaldo = forma; showFormaSaldoDropdown = false }) } }
            }
            
            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) { Checkbox(checked = recebido, onCheckedChange = { recebido = it }); Text("Marcar como recebido", style = MaterialTheme.typography.bodyLarge) }
            
            Spacer(Modifier.height(16.dp))
            Button(onClick = {
                scope.launch {
                    val freteAtualizado = frete.copy(placa = placa, transportadora = transportadora, origem = origem, destino = destino, valorFrete = valorFreteDouble, adiantamento = adiantamentoDouble, formaPgtoAdiant = formaPgtoAdiant, saldoFrete = saldoFrete, formaPgtoSaldo = formaPgtoSaldo, recebido = recebido, updatedAt = System.currentTimeMillis())
                    repo.update(freteAtualizado)
                    onBack()
                }
            }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = GerFrotaColors.Secondary)) { Text("Salvar Alterações") }
        }
    }
}
'''

# 31. PlacasScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/PlacasScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.PlacaEntity
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PlacasScreen(repo: Repository, onBack: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val placas by repo.todasPlacas.collectAsState(initial = emptyList())
    var showAddDialog by remember { mutableStateOf(false) }

    Scaffold(topBar = {
        TopAppBar(title = { Text("Placas") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Voltar") } }, actions = { IconButton(onClick = { showAddDialog = true }) { Icon(Icons.Default.Add, contentDescription = "Adicionar placa") } })
    }, floatingActionButton = {
        FloatingActionButton(onClick = { showAddDialog = true }, containerColor = GerFrotaColors.Secondary) { Icon(Icons.Default.Add, contentDescription = "Adicionar placa") }
    }) { innerPadding ->
        if (placas.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.LocalParking, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.Gray)
                    Spacer(Modifier.height(16.dp))
                    Text("Nenhuma placa cadastrada", style = MaterialTheme.typography.bodyLarge, color = Color.Gray)
                }
            }
        } else {
            LazyColumn(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(placas) { placa ->
                    Card(modifier = Modifier.fillMaxWidth(), shape = MaterialTheme.shapes.medium) {
                        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.LocalParking, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(40.dp))
                            Spacer(Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(placa.placa, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                Text(if (placa.ativa) "Ativa" else "Inativa", style = MaterialTheme.typography.bodySmall, color = if (placa.ativa) GerFrotaColors.Secondary else Color.Gray)
                            }
                            IconButton(onClick = { scope.launch { if (placa.ativa) repo.desativarPlaca(placa.placa) else repo.ativarPlaca(placa.placa) } }) { Icon(if (placa.ativa) Icons.Default.ToggleOn else Icons.Default.ToggleOff, contentDescription = null, tint = if (placa.ativa) GerFrotaColors.Secondary else Color.Gray) }
                            IconButton(onClick = { scope.launch { repo.deletePlacaByNome(placa.placa); Toast.makeText(context, "Placa excluída", Toast.LENGTH_SHORT).show() } }) { Icon(Icons.Default.Delete, contentDescription = "Excluir", tint = GerFrotaColors.Error) }
                        }
                    }
                }
            }
        }
    }

    if (showAddDialog) {
        var placaInput by remember { mutableStateOf("") }
        AlertDialog(onDismissRequest = { showAddDialog = false }, title = { Text("Adicionar Placa") }, text = {
            OutlinedTextField(value = placaInput, onValueChange = { placaInput = it.uppercase() }, label = { Text("Placa (ex: ABC-1234)") }, singleLine = true)
        }, confirmButton = {
            TextButton(onClick = {
                if (placaInput.length >= 7) {
                    scope.launch { repo.insertPlaca(PlacaEntity(placa = placaInput)); Toast.makeText(context, "Placa adicionada!", Toast.LENGTH_SHORT).show() }
                    showAddDialog = false
                }
            }, enabled = placaInput.length >= 7) { Text("Adicionar") }
        }, dismissButton = { TextButton(onClick = { showAddDialog = false }) { Text("Cancelar") } })
    }
}
'''

# 32. BackupScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/BackupScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.LocalBackupManager
import com.gerfrota.fretes.app.data.PreferencesManager
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.drive.BackupDriveResult
import com.gerfrota.fretes.app.drive.DriveBackupManager
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BackupScreen(repo: Repository, onBack: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val driveManager = remember { DriveBackupManager(context) }
    val fretes by repo.fretes.collectAsState(initial = emptyList())
    
    var processando by remember { mutableStateOf(false) }
    var mensagem by remember { mutableStateOf("") }
    var backupPath by remember { mutableStateOf<String?>(null) }
    var lastBackupTime by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        PreferencesManager.getUltimoBackup(context).collect { timestamp ->
            if (timestamp != null) { val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("pt", "BR")); lastBackupTime = sdf.format(Date(timestamp)) }
        }
    }

    Scaffold(topBar = { TopAppBar(title = { Text("Backup e Restauração") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Voltar") } }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Secondary.copy(alpha = 0.1f))) {
                Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.CloudDone, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(32.dp))
                    Spacer(Modifier.width(12.dp))
                    Column {
                        Text("Status do backup", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Text(if (mensagem.isNotEmpty()) mensagem else "Nenhum backup realizado", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                        if (lastBackupTime != null) Text("Último: $lastBackupTime", style = MaterialTheme.typography.bodySmall, color = GerFrotaColors.Secondary)
                    }
                }
            }
            
            Button(onClick = {
                processando = true
                scope.launch {
                    val (sucesso, path) = LocalBackupManager.criarBackupLocal(context, fretes)
                    processando = false
                    if (sucesso) {
                        backupPath = path
                        mensagem = "Backup local criado"
                        PreferencesManager.saveUltimoBackup(context, System.currentTimeMillis())
                        val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("pt", "BR"))
                        lastBackupTime = sdf.format(Date())
                        Toast.makeText(context, "Backup criado!", Toast.LENGTH_SHORT).show()
                    } else {
                        mensagem = "Erro ao criar backup"
                        Toast.makeText(context, "Erro", Toast.LENGTH_SHORT).show()
                    }
                }
            }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = GerFrotaColors.Secondary)) {
                Icon(Icons.Default.Save, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Criar backup local")
            }
            
            Button(onClick = {
                if (backupPath == null) return@Button
                processando = true
                scope.launch {
                    val resultado = driveManager.uploadBackupParaDrive(backupPath!!)
                    processando = false
                    when (resultado) {
                        is BackupDriveResult.Sucesso -> {
                            mensagem = "Backup enviado para Drive"
                            PreferencesManager.saveUltimoBackup(context, System.currentTimeMillis())
                            val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("pt", "BR"))
                            lastBackupTime = sdf.format(Date())
                            Toast.makeText(context, "Backup enviado!", Toast.LENGTH_SHORT).show()
                        }
                        is BackupDriveResult.Error -> {
                            mensagem = "Erro: ${resultado.message}"
                            Toast.makeText(context, "Erro", Toast.LENGTH_LONG).show()
                        }
                    }
                }
            }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = GerFrotaColors.Primary), enabled = backupPath != null) {
                Icon(Icons.Default.CloudUpload, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Enviar para Google Drive")
            }
            
            OutlinedButton(onClick = {
                processando = true
                scope.launch {
                    val resultado = driveManager.downloadBackupDoDrive()
                    processando = false
                    when (resultado) {
                        is BackupDriveResult.Sucesso -> {
                            mensagem = "Backup baixado"
                            Toast.makeText(context, "Backup baixado!", Toast.LENGTH_SHORT).show()
                        }
                        is BackupDriveResult.Error -> {
                            mensagem = "Erro: ${resultado.message}"
                            Toast.makeText(context, "Erro", Toast.LENGTH_LONG).show()
                        }
                    }
                }
            }, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Default.CloudDownload, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Baixar do Google Drive")
            }
        }
    }
}
'''

# 33. RelatoriosScreen.kt
A["app/src/main/java/com/gerfrota/fretes/app/ui/RelatoriosScreen.kt"] = r'''package com.gerfrota.fretes.app.ui

import android.widget.Toast
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gerfrota.fretes.app.data.PdfExporter
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.theme.GerFrotaColors
import kotlinx.coroutines.launch
import java.text.NumberFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RelatoriosScreen(repo: Repository, onBack: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val fretes by repo.fretes.collectAsState(initial = emptyList())
    
    val resumoSaldo by repo.resumoSaldoPorForma.collectAsState(initial = emptyList())
    val resumoAdiant by repo.resumoAdiantamentoPorForma.collectAsState(initial = emptyList())
    
    val nf = NumberFormat.getCurrencyInstance(Locale("pt", "BR"))
    var selectedReport by remember { mutableStateOf<String?>(null) }

    Scaffold(topBar = { TopAppBar(title = { Text("Relatórios") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Voltar") } }) }) { innerPadding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            item { Text("Escolha o relatório", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold) }
            item { ReportCard(title = "Saldos em aberto", subtitle = "Valores pendentes por transportadora", icon = Icons.Default.AccountBalanceWallet, onClick = { selectedReport = "saldos" }) }
            item { ReportCard(title = "Resumo de fretes", subtitle = "Volume, valores e recebimentos", icon = Icons.Default.BarChart, onClick = { selectedReport = "resumo" }) }
            item { ReportCard(title = "Adiantamentos por forma", subtitle = "Resumo das formas de pagamento", icon = Icons.Default.CreditCard, onClick = { selectedReport = "adiantamentos" }) }
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = GerFrotaColors.Secondary.copy(alpha = 0.1f))) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Prévia do período", style = MaterialTheme.typography.titleMedium)
                        Spacer(Modifier.height(8.dp))
                        Text("${fretes.size} fretes", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = GerFrotaColors.Primary)
                        Text("${nf.format(fretes.sumOf { it.saldoFrete })} em aberto", style = MaterialTheme.typography.bodyLarge, color = Color.Gray)
                    }
                }
            }
            item {
                Button(onClick = {
                    if (selectedReport == null) { Toast.makeText(context, "Selecione um tipo de relatório", Toast.LENGTH_SHORT).show(); return@Button }
                    scope.launch {
                        val resultado = when (selectedReport) {
                            "saldos" -> PdfExporter.exportarSaldoPorForma(context, resumoSaldo, fretes)
                            "adiantamentos" -> PdfExporter.exportarAdiantamentoPorForma(context, resumoAdiant, fretes)
                            else -> PdfExporter.exportar(context, fretes)
                        }
                        if (resultado.success) Toast.makeText(context, "Relatório gerado!", Toast.LENGTH_LONG).show()
                        else Toast.makeText(context, "Erro ao gerar relatório", Toast.LENGTH_LONG).show()
                    }
                }, modifier = Modifier.fillMaxWidth().height(56.dp), colors = ButtonDefaults.buttonColors(containerColor = GerFrotaColors.Secondary)) {
                    Icon(Icons.Default.PictureAsPdf, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Gerar PDF", style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}

@Composable
fun ReportCard(title: String, subtitle: String, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth().clickable(onClick = onClick), shape = RoundedCornerShape(12.dp)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, contentDescription = null, tint = GerFrotaColors.Secondary, modifier = Modifier.size(40.dp))
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Medium)
                Text(subtitle, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
        }
    }
}
'''

# 34. MainActivity.kt
A["app/src/main/java/com/gerfrota/fretes/app/MainActivity.kt"] = r'''package com.gerfrota.fretes.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import com.gerfrota.fretes.app.data.AppDatabase
import com.gerfrota.fretes.app.data.AuthManager
import com.gerfrota.fretes.app.data.Repository
import com.gerfrota.fretes.app.ui.LoginScreen
import com.gerfrota.fretes.app.ui.MainScreen
import com.gerfrota.fretes.app.ui.theme.GerFrotaTheme

class MainActivity : ComponentActivity() {
    private val repo by lazy { val db = AppDatabase.get(this); Repository(db.freteDao(), db.placaDao()) }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            GerFrotaTheme {
                val isLogged = AuthManager.isLogged(this)
                val userEmail = AuthManager.getEmail(this) ?: ""
                
                if (isLogged) MainScreen(repo = repo, userEmail = userEmail, onLogout = { AuthManager.logout(this); recreate() })
                else LoginScreen(repo = repo, onLoginSuccess = { recreate() })
            }
        }
    }
}
'''

# 35. Recursos
A["app/src/main/res/drawable/ic_truck_logo.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#102A43" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="#0F766E" android:pathData="M20,60 L20,40 L60,40 L60,50 L75,50 L85,60 L85,72 L80,72 A8,8 0 0,1 64,72 L44,72 A8,8 0 0,1 28,72 L20,72 Z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M36,72 m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0"/>
    <path android:fillColor="#FFFFFF" android:pathData="M72,72 m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0"/>
    <path android:fillColor="#F59E0B" android:pathData="M64,52 L73,52 L80,60 L64,60 Z"/>
</vector>
'''

A["app/src/main/res/values/colors.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#102A43</color>
    <color name="primary">#102A43</color>
    <color name="secondary">#0F766E</color>
    <color name="tertiary">#F59E0B</color>
    <color name="error">#B42318</color>
</resources>
'''

A["app/src/main/res/values/strings.xml"] = r'''<resources><string name="app_name">GerFrota Fretes</string></resources>
'''

A["app/src/main/res/values/themes.xml"] = r'''<resources><style name="Theme.GerFrotaFretes" parent="android:Theme.Material.Light.NoActionBar"/></resources>
'''

A["app/src/main/res/xml/file_paths.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path name="external_files" path="."/>
    <external-files-path name="external_files2" path="."/>
    <cache-path name="cache" path="."/>
    <files-path name="files" path="."/>
</paths>
'''

A["app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_truck_logo"/>
</adaptive-icon>
'''

A["app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_truck_logo"/>
</adaptive-icon>
'''

A["app/proguard-rules.pro"] = r'''# GerFrota Fretes - Regras ProGuard / R8
-keep class com.gerfrota.fretes.app.data.** { *; }
-keep class com.google.api.** { *; }
-keep class com.google.auth.** { *; }
-keepattributes Signature
-keepattributes *Annotation*
-keep class sun.misc.Unsafe { *; }
-keep class com.google.gson.stream.** { *; }
-keep class androidx.compose.** { *; }
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Regras para lidar com dependências opcionais do Apache HTTP Client (Google API Client)
-dontwarn javax.naming.**
-dontwarn org.ietf.jgss.**
-dontwarn org.apache.http.**
-keep class javax.naming.** { *; }
-keep class org.ietf.jgss.** { *; }
'''

A["CHANGELOG.md"] = r'''# Changelog - GerFrota Fretes
## [1.0.0] - 2026-08-21
### Adicionado
- Design System Material 3 completo com modo escuro
- Navegação inferior (Início, Fretes, Financeiro, Mais)
- Dashboard operacional com indicadores comparativos
- Formulário de frete com máscara monetária
- Validações financeiras e confirmação/desfazer
- Busca avançada e filtros persistentes
- Relatórios contextuais em PDF
- Backup local e Google Drive com status visível
- 9 Formas de Pagamento específicas
- Testes unitários e de migração
- Acessibilidade completa
- ProGuard para release
### Melhorado
- Contraste de cores para acessibilidade
- Áreas de toque em todos os botões (48dp)
- ContentDescription em ícones
- Suporte a fonte ampliada
### Corrigido
- Cálculo de saldo com valores negativos
- Validação de adiantamento maior que frete
- Filtros preservados ao retornar de edição
### Segurança
- Microfone solicitado apenas no contexto de uso
- Confirmação forte antes de restaurar backup
- Validação de arquivo antes de importação
'''

A["README.md"] = r'''# GerFrota Fretes
Aplicativo Android para gestão de fretes e transportes.

## Funcionalidades
- ✅ Cadastro de fretes com máscara monetária
- ✅ Controle por placa (5 placas pré-cadastradas)
- ✅ 9 formas de pagamento específicas
- ✅ Saldos a receber por transportadora
- ✅ Relatórios em PDF (compartilhamento WhatsApp/E-mail)
- ✅ Backup local e Google Drive
- ✅ Busca e filtros avançados
- ✅ Modo escuro
- ✅ Acessibilidade completa

## Tecnologias
- Kotlin
- Jetpack Compose
- Material 3
- Room Database
- Google Drive API
- DataStore Preferences

## Instalação
1. Clone o repositório
2. Abra no Android Studio
3. Execute `./gradlew assembleDebug`
4. Instale o APK em `app/build/outputs/apk/debug/`

## Build com GitHub Actions
1. Faça push para a branch `main`
2. GitHub Actions compilará automaticamente
3. Baixe o APK em Actions → Artifacts

## Changelog
Veja [CHANGELOG.md](CHANGELOG.md) para histórico de versões.

## Licença
Proprietário - GerFrota Fretes
'''

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================
def criar_projeto():
    print("=" * 60)
    print("  GERADOR DO PROJETO GerFrota Fretes v1.0")
    print("  NOVO APP - IDENTIFICADOR ÚNICO")
    print("=" * 60)
    print()
    
    if os.path.exists(PROJETO):
        resposta = input(f"A pasta '{PROJETO}' já existe. Deseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("Operação cancelada.")
            return
        import shutil
        shutil.rmtree(PROJETO)
    
    total = len(A)
    criado = 0
    
    for caminho, conteudo in A.items():
        caminho_completo = os.path.join(PROJETO, caminho)
        diretorio = os.path.dirname(caminho_completo)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(conteudo.lstrip('\n'))
        criado += 1
        print(f"  [{criado}/{total}] {caminho}")
    
    print()
    print("=" * 60)
    print("  PROJETO CRIADO COM SUCESSO!")
    print("=" * 60)
    print()
    print(f"  Pasta: {os.path.abspath(PROJETO)}")
    print(f"  Arquivos: {criado}")
    print()
    print("  IDENTIFICADOR DO APP: com.gerfrota.fretes.app")
    print("  VERSÃO: 1.0.0")
    print()
    print("  FUNCIONALIDADES:")
    print("  ✓ Design System Material 3 com modo escuro")
    print("  ✓ Navegação inferior (Início, Fretes, Financeiro, Mais)")
    print("  ✓ Dashboard operacional com indicadores")
    print("  ✓ Formulário de frete com máscara monetária")
    print("  ✓ Validações financeiras e confirmação")
    print("  ✓ Busca e filtros persistentes")
    print("  ✓ Relatórios contextuais em PDF")
    print("  ✓ Backup local e Google Drive")
    print("  ✓ 9 Formas de Pagamento")
    print("  ✓ Testes unitários")
    print("  ✓ ProGuard para release")
    print()
    print("  PRÓXIMOS PASSOS:")
    print("  1. Commit e push no GitHub")
    print("  2. GitHub Actions compilará automaticamente")
    print("  3. Baixe o APK em Actions > Artifacts")
    print("=" * 60)

if __name__ == "__main__":
    try:
        criar_projeto()
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro: {e}")
        sys.exit(1)
