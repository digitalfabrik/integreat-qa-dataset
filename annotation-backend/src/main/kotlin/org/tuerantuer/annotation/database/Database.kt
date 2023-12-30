package org.tuerantuer.annotation.database

import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.database.annotations.Annotations
import org.tuerantuer.annotation.database.questions.Questions

class Database {
    companion object {
        fun setup(): Database {
            val database = Database.connect(
                url = "jdbc:postgresql://localhost:5432/annotations",
                driver = "org.postgresql.Driver",
                user = "postgres",
                password = "postgres",
                setupConnection = {
                    it.prepareStatement("SET TIME ZONE 'UTC';").executeUpdate()
                }
            )
            transaction {
                SchemaUtils.create(Questions, Annotations)
            }
            return database
        }
    }

}
