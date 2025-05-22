#ifndef BRANCH_MARKOV_H
#define BRANCH_MARKOV_H

#include <array>

#include "address.h"
#include "modules.h"
#include "msl/fwcounter.h"

class markov : champsim::modules::branch_predictor
{
  struct Counter {
    uint64_t taken = 0;
    uint64_t not_taken = 0;
  };

  [[nodiscard]] static constexpr auto hash(champsim::address ip) { return ip.to<unsigned long>() % PRIME; }

  static constexpr std::size_t TABLE_SIZE = 16384;
  static constexpr std::size_t PRIME = 16381;
  static constexpr std::size_t BITS = 2;

  std::array<Counter, TABLE_SIZE> markov_table;

public:
  using branch_predictor::branch_predictor;

  // void initialize_branch_predictor();
  bool predict_branch(champsim::address ip);
  void last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type);
};

#endif
