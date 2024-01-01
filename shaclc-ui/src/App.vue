<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Card from 'primevue/card'
import Dropdown, { type DropdownChangeEvent } from 'primevue/dropdown'
import BlockUI from 'primevue/blockui'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import { Codemirror } from 'vue-codemirror'

import { usePyodide } from './composables/pyodide'
import pyconvert from './assets/convert.py?raw'
import { examples } from '@/shaclcExamples'

let { initPyodide, isPyodideLoading, pyodide } = usePyodide(['shaclc'])

onMounted(async () => {
  await initPyodide()

  pyodide.value.runPython(pyconvert)
})

type Example = { name: string; code: string }

const toast = useToast()
const isLoading = ref(false)
const isFetching = ref(false)
const shaclcStr = ref('')
const resultStr = ref('')
const selectedExample = ref<null | Example>(null)
const exampleValues = ref<Example[]>(examples)

watch([isPyodideLoading, isFetching], ([newIsPyodideLoading, newIsFetching]) => {
  isLoading.value = newIsPyodideLoading || newIsFetching
})

const handleError = (errorMsg: string) => {
  toast.add({
    severity: 'error',
    summary: 'Failed to fetch resource',
    detail: errorMsg,
    life: 5000
  })
}

watch(selectedExample, async (newExample) => {
  if (newExample != null) {
    isFetching.value = true
    try {
      const response = await fetch(newExample?.code)
      if (response.ok) {
        shaclcStr.value = await response.text()
      } else {
        handleError(`Failed to retrieve example from ${response.url}`)
      }
    } catch (error: any) {
      handleError(error)
    } finally {
      isFetching.value = false
    }
  }
})

const handleClearButtonClick = () => {
  selectedExample.value = null
  shaclcStr.value = ''
  handleConvertButtonClick()
}

const handleConvertButtonClick = () => {
  const pythonCallStr = `convert("""${shaclcStr.value}""")`
  resultStr.value = pyodide.value.runPython(pythonCallStr)
}
</script>

<template>
  <Toast />
  <BlockUI :blocked="isLoading" fullScreen />
  <div
    v-if="isLoading"
    class="absolute opacity-70 bg-gray-200 p-overflow-hidden w-screen h-screen"
  ></div>
  <div
    v-if="isLoading"
    class="absolute opacity-70 bg-gray-300 p-overflow-hidden m-0 top-[50%] left-[50%] -translate-x-1/2 -translate-y-1/2"
  >
    <p class="p-3">Loading...</p>
  </div>

  <div class="container mx-auto space-y-4 py-4">
    <h1 class="text-4xl font-bold">SHACL Compact Syntax Playground</h1>
    <p>
      A Python implementation of the
      <a
        href="https://w3c.github.io/shacl/shacl-compact-syntax/"
        target="_blank"
        class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
        >SHACL Compact Syntax</a
      >
      running in the browser.
    </p>
    <p>This playground converts shapes in the SHACL Compact Syntax to RDF.</p>
    <p>
      Source code:
      <a
        href="https://github.com/edmondchuc/shaclc"
        target="_blank"
        class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
        >https://github.com/edmondchuc/shaclc</a
      >
    </p>

    <hr />

    <Dropdown
      v-model="selectedExample"
      option-label="name"
      :options="exampleValues"
      show-clear
      filter
      placeholder="Select an example"
      @change="(e: DropdownChangeEvent) => e.value === null && handleClearButtonClick()"
    ></Dropdown>

    <div>
      <Codemirror
        v-model="shaclcStr"
        placeholder="... or enter your own custom input"
        :style="{ height: '200px' }"
      />
    </div>

    <button
      v-if="resultStr"
      @click="handleClearButtonClick"
      class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
    >
      Clear
    </button>
    <button
      v-if="shaclcStr"
      @click="handleConvertButtonClick"
      class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
    >
      Convert
    </button>

    <Card
      v-if="resultStr"
      :pt="{
        body: 'shadow-sm p-3 bg-slate-50 border'
      }"
    >
      <template #title>
        <h2 class="text-2xl font-bold pt-2">Result</h2>
      </template>
      <template #content>
        <Codemirror v-model="resultStr" disabled />
      </template>
    </Card>
  </div>
</template>
