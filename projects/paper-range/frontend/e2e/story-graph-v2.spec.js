import { expect, test } from '@playwright/test'

async function runCommand(page, command) {
  const input = page.getByTestId('command-input')
  await input.fill(command)
  await page.getByTestId('execute-command').click()
}

test('player can complete the two-layer investigation branch in the browser', async ({ page }) => {
  await page.goto('/')

  await page.getByTestId('scenario-abandoned-lab').click()
  await page.getByTestId('start-operation').click()

  await expect(page.getByTestId('game-shell')).toBeVisible()
  await expect(page.getByTestId('story-node-value')).toHaveText('recon')
  await expect(page.getByTestId('stream-state')).toContainText(/SSE (LIVE|RECONNECTING|CONNECTING)/)

  await runCommand(page, 'nmap -p- 10.10.10.10')
  await expect(page.getByTestId('story-node-value')).toHaveText('web-investigation')

  await runCommand(page, 'curl http://10.10.10.10')
  await expect(page.getByTestId('story-node-value')).toHaveText('approach-decision')
  await expect(page.getByTestId('approach-choice')).toBeVisible()

  await page.getByTestId('approach-focused').click()
  await expect(page.getByTestId('story-node-value')).toHaveText('path-enumeration')
  await expect(page.getByTestId('world-tags')).toContainText('low-noise-recon')

  await runCommand(page, 'dirsearch -u http://10.10.10.10')
  await expect(page.getByTestId('story-node-value')).toHaveText('evidence-strategy')
  await expect(page.getByTestId('evidence-choice')).toBeVisible()

  await page.getByTestId('evidence-correlate').click()
  await expect(page.getByTestId('story-node-value')).toHaveText('correlation-work')
  await expect(page.getByTestId('correlation-checks')).toBeVisible()

  await page.getByTestId('correlation-log').click()
  await expect(page.getByTestId('investigation-checks')).toContainText('log-query')
  await expect(page.getByTestId('story-node-value')).toHaveText('correlation-work')

  await page.getByTestId('correlation-asset').click()
  await expect(page.getByTestId('investigation-checks')).toContainText('asset-map')
  await expect(page.getByTestId('story-node-value')).toHaveText('evidence-review')
  await expect(page.getByTestId('world-tags')).toContainText('correlated-evidence')
  await expect(page.getByTestId('terminal-log')).toContainText('network_io=none')
})

test('direct evidence route skips the correlation node', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('scenario-abandoned-lab').click()
  await page.getByTestId('start-operation').click()

  await runCommand(page, 'nmap -p- 10.10.10.10')
  await runCommand(page, 'curl http://10.10.10.10')
  await page.getByTestId('approach-focused').click()
  await runCommand(page, 'dirsearch -u http://10.10.10.10')

  await page.getByTestId('evidence-direct').click()
  await expect(page.getByTestId('story-node-value')).toHaveText('evidence-review')
  await expect(page.getByTestId('story-step-correlation-work')).toHaveClass(/skipped/)
  await expect(page.getByTestId('world-tags')).toContainText('direct-evidence-route')
})
