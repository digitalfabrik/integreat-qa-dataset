package org.tuerantuer.annotation

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.core.subcommands
import com.github.ajalt.clikt.parameters.arguments.argument
import com.github.ajalt.clikt.parameters.arguments.check
import com.github.ajalt.clikt.parameters.options.flag
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.types.file
import com.github.ajalt.clikt.parameters.types.int
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.SchemaUtils
import org.tuerantuer.annotation.database.*
import org.tuerantuer.annotation.models.Row

class Backend : CliktCommand() {
    override fun run() = Unit
}

class Run : CliktCommand(help = "Run backend") {
    private val dev by option("--dev").flag()

    override fun run() {
        start(dev)
    }
}

class Import : CliktCommand(help = "Import questions") {
    private val dataset by argument().file().check("only json files supported") { it.extension == "json" }

    override fun run() {
        Database.setup()
        insertRows(Json.decodeFromString<List<Row>>(dataset.readText()))
    }
}

class ArchiveQuestion : CliktCommand(help = "Archive question") {

    private val questionId by argument().int()

    override fun run() {
        Database.setup()
        archiveQuestion(questionId)
    }
}

class DeleteAnnotations : CliktCommand(help = "Delete annotations") {
    private val user by option()

    override fun run() {
        Database.setup()
        deleteAnnotations(user)
    }
}

class Drop : CliktCommand(help = "Drop all tables") {
    override fun run() {
        Database.setup()
        drop()
    }
}

fun main(args: Array<String>) =
    Backend().subcommands(Run(), Import(), ArchiveQuestion(), DeleteAnnotations(), Drop()).main(args)
