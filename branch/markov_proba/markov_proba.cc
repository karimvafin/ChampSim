#include "markov_proba.h"

bool markov_proba::predict_branch(champsim::address ip)
{
  auto& counter = markov_table[hash(ip)];
  uint64_t total = counter.taken + counter.not_taken;
  if (total == 0) return true;
  double prob_taken = static_cast<double>(counter.taken) / total;
  std::uniform_real_distribution<double> dist(0.0, 1.0);
  return dist(rng) < prob_taken;
}

void markov_proba::last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type)
{
  auto& counter = markov_table[hash(ip)];
  if (taken)
    counter.taken++;
  else
    counter.not_taken++;
}
