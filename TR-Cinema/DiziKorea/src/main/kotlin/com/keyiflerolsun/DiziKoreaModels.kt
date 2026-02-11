// ! Bu araç @ayhankucuk tarafından | @Özel CloudStream Havuzu için yazılmıştır.

package com.ayhankucuk

import com.fasterxml.jackson.annotation.JsonProperty

data class KoreaSearch(
    @JsonProperty("theme") val theme: String
)