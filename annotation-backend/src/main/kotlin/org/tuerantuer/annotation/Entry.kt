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
import org.tuerantuer.annotation.database.Database
import org.tuerantuer.annotation.database.archiveQuestion
import org.tuerantuer.annotation.database.deleteAnnotations
import org.tuerantuer.annotation.database.insertRows
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

class ArchiveQuestions : CliktCommand(help = "Archive question") {

    private val questionId by argument().int()

    override fun run() {
        Database.setup()
        archiveQuestion(questionId)
    }
}

class DeleteAnnotations : CliktCommand(help = "Archive question") {
    override fun run() {
        Database.setup()
        deleteAnnotations()
    }
}

fun main(args: Array<String>) =
    Backend().subcommands(Run(), Import(), ArchiveQuestions(), DeleteAnnotations()).main(args)
