package org.tuerantuer.annotation.models

import kotlinx.serialization.Serializable

@Serializable
data class WithId<T>(
    val id: Int,
    val value: T
)
