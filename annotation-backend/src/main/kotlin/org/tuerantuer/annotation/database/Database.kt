package org.tuerantuer.annotation.database

import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction
import java.io.File

class Database {
    companion object {
        fun setup(): Database {
            val credentialsFile = File("/etc/annotations.conf")
            val credentials =
                if (credentialsFile.exists()) Json.decodeFromString<Map<String, String>>(credentialsFile.readText()) else null
            val postgresHost = credentials?.get("POSTGRES_HOST") ?: "localhost:5432"
            val postgresDatabase = credentials?.get("POSTGRES_DATABASE") ?: "annotations"
            val postgresUser = credentials?.get("POSTGRES_USER") ?: "postgres"
            val postgresPassword = credentials?.get("POSTGRES_PASSWORD") ?: "postgres"

            val database = Database.connect(
                url = "jdbc:postgresql://$postgresHost/$postgresDatabase",
                driver = "org.postgresql.Driver",
                user = postgresUser,
                password = postgresPassword,
                setupConnection = {
                    it.prepareStatement("SET TIME ZONE 'UTC';").executeUpdate()
                }
            )
            transaction {
                SchemaUtils.create(Rows, Questions, Annotations)
            }
            return database
        }
    }
}
