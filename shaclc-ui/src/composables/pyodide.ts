import { ref } from 'vue'
import { loadPyodide } from 'pyodide'

const indexURL = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'

export function usePyodide(packages: string[] = []) {
  const pyodide = ref<any>(null)
  const isPyodideLoading = ref<boolean>(false)

  const initPyodide = async () => {
    isPyodideLoading.value = true

    pyodide.value = await loadPyodide({
      indexURL: indexURL
    })

    if (packages && pyodide.value != null) {
      await pyodide.value.loadPackage('setuptools')
      await pyodide.value.loadPackage('micropip')
      const micropip = pyodide.value.pyimport('micropip')

      for (const p of packages) {
        await micropip.install(p)
      }
    }

    isPyodideLoading.value = false
  }

  return { pyodide, initPyodide, isPyodideLoading }
}
