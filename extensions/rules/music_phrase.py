# coding: utf-8
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Rules for MusicPhrase objects."""

__author__ = 'Michael Wagner'

from extensions.rules import base


NOTE_MAP = {'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69,
            'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79,
            'A5': 81}


def get_midi_note_value(note):
    if isinstance(note, dict):
        if note['readableNoteName'] in NOTE_MAP:
            return NOTE_MAP[note['readableNoteName']]
    else:
        raise Exception('Invalid music note %s.' % note)


def convert_sequence_to_midi(sequence):
    return [get_midi_note_value(note) for note in sequence]


class Equals(base.MusicPhraseRule):
    description = 'is equal to {{x|MusicPhrase}}'

    def _evaluate(self, subject):
        return (convert_sequence_to_midi(subject) == 
                convert_sequence_to_midi(self.x))


class IsLongerSequence(base.MusicPhraseRule):
    description = 'is a longer sequence than {{x|MusicPhrase}}'

    def _evaluate(self, subject):
        return (len(convert_sequence_to_midi(subject)) > 
                len(convert_sequence_to_midi(self.x)))

        
class IsEqualToExceptFor(base.MusicPhraseRule):
    description = ('is equal to {{x|MusicPhrase}} '
                   'except for {{k|NonnegativeInt}} notes')

    def _evaluate(self, subject):
        midi_target_sequence = convert_sequence_to_midi(self.x)
        midi_user_sequence = convert_sequence_to_midi(subject)
        # target_sequence_length = len(midi_target_sequence)
        # user_sequence_length = len(midi_user_sequence)
        counter = 0
        num_correct_notes_needed = len(midi_target_sequence) - self.k
        for i in range(min(len(midi_target_sequence), len(midi_user_sequence))):
            if midi_user_sequence[i] == midi_target_sequence[i]:
                counter += 1
        return counter >= num_correct_notes_needed


class IsTranspositionOf(base.MusicPhraseRule):
    description = ('is a transposition of {{x|MusicPhrase}} '
                   'by {{y|Int}} semitones')

    def _evaluate(self, subject):
        target_sequence_length = len(self.x)
        if (len(subject) == target_sequence_length):
            midi_target_sequence = convert_sequence_to_midi(self.x)
            midi_user_sequence = convert_sequence_to_midi(subject)
            is_transposition = True
            for i in range(target_sequence_length):
                if midi_user_sequence[i] - self.y != midi_target_sequence[i]:
                    return False
            return is_transposition
        else:
            return False


class IsTranspositionOfExceptFor(base.MusicPhraseRule):
    description = ('is a transposition of {{x|MusicPhrase}} '
                   'by {{y|Int}} semitones '
                   'except for {{k|NonnegativeInt}} notes')

    def _evaluate(self, subject):
        counter = 0
        midi_target_sequence = convert_sequence_to_midi(self.x)
        midi_user_sequence = convert_sequence_to_midi(subject)
        target_sequence_length = len(midi_target_sequence)
        if (len(midi_user_sequence) == target_sequence_length or
            len(midi_user_sequence) >= target_sequence_length - self.k):        
            num_correct_notes_needed = target_sequence_length - self.k
            if len(midi_user_sequence) > 1:
                for i in range(target_sequence_length):
                    if midi_user_sequence[i] - self.y == midi_target_sequence[i]:
                        counter += 1
            return counter >= num_correct_notes_needed
        else:
            return False
